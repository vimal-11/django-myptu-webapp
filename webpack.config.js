module.exports = {
    module: {
      rules: [
        {
          test: /\.js$/,
          exclude: /node_modules/,
          use: {
            loader: "babel-loader"
          }
        }, 
        /* for css and js styles files */ 
        {
          test: /\.css$/i,
          use: ['style-loader', 'css-loader'],
        } ,
    /* for files and images */    
        {
          test: /\.(jpe?g|png|gif|woff|woff2|otf|eot|ttf|svg)(\?[a-z0-9=.]+)?$/,
          use: [
              {
                  loader: 'url-loader',
                  options: {
                      limit: 1000,
                      name : 'assets/img/[name].[ext]'
                  }
              }
          ]
      }
      ]
    }
  }
