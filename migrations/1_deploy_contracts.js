const AssetToken = artifacts.require("AssetToken");
module.exports = function (deployer) {
    const name = "AssetToken";
    const symbol = "AST";
    const initialSupply = 1000000; // 1 million tokens
    deployer.deploy(AssetToken, name, symbol, initialSupply);
  };