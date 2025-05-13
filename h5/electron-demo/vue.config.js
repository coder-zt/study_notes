const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  runtimeCompiler: true, //[Vue warn]: You are using the runtime-only build of Vue where the template compiler is not available
})
