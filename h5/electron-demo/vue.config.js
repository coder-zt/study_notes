const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    open: true,
    host: 'localhost',
    port: 8080,
    proxy: {
        '/abc': {    //1
            target: 'https://localhost:8080',    //2
            changOrigin: true,
            pathRewrite: {    //3
                '^/abc': ''
            }
        }
    }
}
})
