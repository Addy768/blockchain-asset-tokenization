pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";

contract AssetToken is ERC721 {
    struct TokenMetadata {
        string name;
        string description;
        string imageURI;
    }

    mapping(uint256 => TokenMetadata) public tokenMetadata;

    constructor() ERC721("AssetToken", "AST") {}

    function mint(
        address to,
        uint256 tokenId,
        string memory name,
        string memory description,
        string memory imageURI
    ) public {
        _mint(to, tokenId);
        tokenMetadata[tokenId] = TokenMetadata(name, description, imageURI);
    }

    function getTokenMetadata(uint256 tokenId)
        public
        view
        returns (TokenMetadata memory)
    {
        return tokenMetadata[tokenId];
    }
    function burn(uint256 tokenId) public {
    require(ownerOf(tokenId) == msg.sender, "You do not own this token.");
    _burn(tokenId);
    }

}
