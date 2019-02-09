module.exports = [{
    entry: "./src/botDetect.js",
    output: {
      filename: "dist/content.bundle.js"
    },
    watch: true
},
{
    entry: "./src/botExtension.js",
    output: {
      filename: "dist/background.bundle.js"
    },
    watch: true
}]