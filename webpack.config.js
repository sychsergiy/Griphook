const path = require("path");

module.exports = {
  entry: "./griphook/client/react/index.js",
  output: {
    path: path.join(__dirname, "griphook/client/static/bundles"),
    filename: "filters_bundle.js"
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader"
        }
      }
    ]
  },
  plugins: []
};
