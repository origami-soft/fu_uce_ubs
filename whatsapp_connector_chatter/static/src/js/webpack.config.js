const path = require('path');
const dirTree = require("directory-tree");
const TerserPlugin = require('terser-webpack-plugin');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');
const generate = require('generate-file-webpack-plugin');
const path_module = '../../../../../whatsapp_app/whatsapp_connector_chatter/';

function get_files_to_compile() {
    const globalTree = dirTree(__dirname, {extensions:/\.js$/});
    let findFiles;
    const out = []
    
    findFiles = tree => {
        tree.children.forEach(child => {
            if (child.type == 'directory' && child.name != 'node_modules') {
                findFiles(child)
            } else {
                if(child.extension == '.js' && child.name != 'webpack.config.js') {
                    out.push(child.path.replace(__dirname + '/', ''))
                }
            }
        })
    }
    findFiles(globalTree)
    return out;
}

const source_code = get_files_to_compile()


module.exports = {
  entry: {
    app: source_code.map(x => path.resolve(__dirname, './' + x)),
  },
  output: {
    filename: '[name].js',
    path: path.resolve(__dirname, path_module + 'static/src/js/')
  },
  optimization: {
    minimizer: [
      new TerserPlugin({
        terserOptions: {
          mangle: false,
          output: {
            beautify: true
          }
        },
      }),
    ],
  },
  plugins: [
    new CleanWebpackPlugin({
        dry: false,
        cleanAfterEveryBuildPatterns: source_code.map(x => path.resolve(__dirname, path_module + 'static/src/js/' + x)).concat([
            path.resolve(__dirname, path_module + 'static/src/js/package.json'),
            path.resolve(__dirname, path_module + 'static/src/js/webpack.config.js'),
        ]),
        dangerouslyAllowCleanPatternsOutsideProject: true,
    }),
    generate({
      file: path.resolve(__dirname, path_module + 'views') + '/include_template.xml',
      content: include_xml()
    })
  ]
};

function include_xml() {
let out = 
`<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <template id="assets_backend" name="acrux chatter assets" inherit_id="web.assets_backend">
        <xpath expr="." position="inside">
            <script type="text/javascript" src="/whatsapp_connector_chatter/static/src/js/app.js" />

            <link rel="stylesheet" href="/whatsapp_connector_chatter/static/src/css/chatter.css" type="text/css"/>
        </xpath>
    </template>
</odoo>
`;
return out
}
