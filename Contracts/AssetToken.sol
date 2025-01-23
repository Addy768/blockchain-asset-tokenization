// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract AssetToken is ERC20 {
    address public owner;

    constructor(string memory name, string memory symbol, uint256 initialSupply) ERC20(name, symbol) {
        owner = msg.sender;
        _mint(msg.sender, initialSupply * (10 ** decimals()));
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Only the owner can perform this action");
        _;
    }

    function mint(address to, uint256 amount) public onlyOwner {
        _mint(to, amount);
    }

    function burn(address from, uint256 amount) public onlyOwner {
        _burn(from, amount);
    }
}
