// SPDX-License-Identifier: MIT


pragma solidity ^0.8.10;

import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/token/ERC721/IERC721.sol";
import "@openzeppelin/contracts/token/ERC1155/IERC1155.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract SimpleWill is Ownable {
    using SafeERC20 for IERC20;

    address beneficiary;
    uint256 releaseTime;

    constructor(
        address beneficiary_,
        uint256 releaseTime_)
    {
        beneficiary = beneficiary_;
        releaseTime = releaseTime_;
    }

    event ReleasedERC20(address owner, address beneficiary, address tokenERC20Address);
    event ReleasedERC721(address owner, address beneficiary, address tokenERC721Address);
    event ReleasedERC1155(address owner, address beneficiary, address tokenERC1155Address);
    event NewReleaseTime(uint releaseTime);
    event NewBeneficiary(address beneficiary);

    function getBeneficiary() public view returns (address) {
        return beneficiary;
    }

    function getReleaseTime() public view returns (uint256) {
        return releaseTime;
    }

    function setNewBeneficiary(address newBeneficiary) public onlyOwner returns (address) {
        beneficiary = newBeneficiary;
        emit NewBeneficiary(beneficiary);
        return beneficiary;
    }

    function setNewReleaseTime(uint256 newReleaseTime) public onlyOwner returns (uint256) { // external?
        releaseTime = newReleaseTime;
        emit NewReleaseTime(releaseTime);
        return releaseTime;
    }

    function releaseERC20(IERC20 tokenERC20) external {
        require(block.timestamp >= releaseTime,  "Current time is before release time");
        uint256 balance =  tokenERC20.balanceOf(owner());
        if ( balance > 0 ) {
            uint256 allowed = tokenERC20.allowance(owner(), address(this));
            if ( allowed > balance) {
                tokenERC20.safeTransferFrom(owner(), beneficiary, balance);
            } else {
                tokenERC20.safeTransferFrom(owner(), beneficiary, allowed);
            }
        }
        emit ReleasedERC20(owner(), beneficiary, address(tokenERC20));
    }

    function releaseERC721(IERC721 tokenERC721, uint256[] calldata tokenIdList) external {
        require(block.timestamp >= releaseTime,  "Current time is before release time");
        for (uint i = 0; i < tokenIdList.length; i++) {
            tokenERC721.safeTransferFrom(owner(), beneficiary, tokenIdList[i]);
            }
        emit ReleasedERC721(owner(), beneficiary, address(tokenERC721));
    }

    function releaseERC1155(IERC1155 tokenERC1155, uint256[] calldata tokenIdList, uint256[] calldata value) external {
        require(block.timestamp >= releaseTime,  "Current time is before release time");
        tokenERC1155.safeBatchTransferFrom(owner(), beneficiary, tokenIdList, value, bytes(''));
        emit ReleasedERC1155(owner(), beneficiary, address(tokenERC1155));
    }

    function batchRelease(
        IERC20[] calldata tokenERC20List,
        IERC721[] calldata tokenERC721List,
        IERC1155[] calldata tokenERC1155List,
        uint[][] calldata ERC721tokenIdLists,
        uint[][] calldata ERC1155tokenIdLists,
        uint[][] calldata valueLists
    )
    external
    {
        for (uint i = 0; i < tokenERC20List.length; i++) {
            this.releaseERC20(tokenERC20List[i]);
        }
        for (uint i = 0; i < tokenERC721List.length; i++) {
            this.releaseERC721(tokenERC721List[i], ERC721tokenIdLists[i]);
        }
        for (uint i = 0; i < tokenERC1155List.length; i++) {
            this.releaseERC1155(tokenERC1155List[i], ERC1155tokenIdLists[i], valueLists[i]);
        }
    }
}