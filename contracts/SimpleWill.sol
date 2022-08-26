// SPDX-License-Identifier: MIT

pragma solidity ^0.8.11;

import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/token/ERC721/IERC721.sol";
import "@openzeppelin/contracts/token/ERC1155/IERC1155.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

/**
 * @title SimpleWill
 * @author DimaKush
 * @notice Contract is used as will: delpoyer of contract allow tokens to SimpleWill that can be tranfered from deployer to beneficiary
 * only after release time. Testator should extend release time to prove his access to account.
 */
contract SimpleWill is Ownable {
    using SafeERC20 for IERC20;

    address beneficiary;
    uint256 releaseTime;

    /**
     * @notice Constructor
     * @param _beneficiary: address of tokens receiver
     * @param _releaseTime: UNIX time when tokens can be released
     */
    constructor(address _beneficiary, uint256 _releaseTime) {
        beneficiary = _beneficiary;
        releaseTime = _releaseTime;
    }

    event ReleasedERC20(
        address owner,
        address beneficiary,
        address tokenERC20Address
    );
    event ReleasedERC721(
        address owner,
        address beneficiary,
        address tokenERC721Address
    );
    event ReleasedERC1155(
        address owner,
        address beneficiary,
        address tokenERC1155Address
    );
    event NewReleaseTime(uint releaseTime);
    event NewBeneficiary(address beneficiary);
    event ERC20Recovery(address _token, uint balance);

    /**
     * @notice Recover ERC20 tokens that was sent mistakenly
     */
    function recoverERC20(address _token) external onlyOwner {
        uint balance = IERC20(_token).balanceOf(address(this));
        require(balance != 0, "Cannot recover zero balance");
        IERC20(_token).safeTransfer(address(msg.sender), balance);
        emit ERC20Recovery(_token, balance);
    }

    function getBeneficiary() public view returns (address) {
        return beneficiary;
    }

    function getReleaseTime() public view returns (uint) {
        return releaseTime;
    }

    function setNewBeneficiary(address newBeneficiary)
        public
        onlyOwner
        returns (address)
    {
        beneficiary = newBeneficiary;
        emit NewBeneficiary(beneficiary);
        return beneficiary;
    }

    function setNewReleaseTime(uint newReleaseTime)
        public
        onlyOwner
        returns (uint)
    {
        require(
            newReleaseTime > block.timestamp,
            "newReleaseTime < block.timestamp"
        );
        releaseTime = newReleaseTime;
        emit NewReleaseTime(releaseTime);
        return releaseTime;
    }

    /**
     * @notice Transfer ERC20 tokens from owner to beneficiary.
     * @dev Callable by anybody
     */
    function releaseERC20(IERC20 tokenERC20) external {
        require(
            block.timestamp >= releaseTime,
            "newReleaseTime < block.timestamp"
        );
        uint balance = tokenERC20.balanceOf(owner());
        require(balance != 0, "No ERC20 tokens to release");
        uint allowed = tokenERC20.allowance(owner(), address(this));
        require(allowed != 0, "ERC20 zero allowance");
        if (allowed > balance) {
            tokenERC20.safeTransferFrom(owner(), beneficiary, balance);
        } else {
            tokenERC20.safeTransferFrom(owner(), beneficiary, allowed);
        }

        emit ReleasedERC20(owner(), beneficiary, address(tokenERC20));
    }

    /**
     * @notice Transfer ERC721 tokens from owner to beneficiary.
     * @dev Callable by anybody
     */
    function releaseERC721(IERC721 tokenERC721, uint[] calldata tokenIdList)
        external
    {
        require(
            block.timestamp >= releaseTime,
            "Current time is before release time"
        );
        require(
            tokenERC721.isApprovedForAll(owner(), address(this)),
            "ERC721 zero allowance"
        );
        for (uint i = 0; i < tokenIdList.length; i++) {
            tokenERC721.safeTransferFrom(owner(), beneficiary, tokenIdList[i]);
        }
        emit ReleasedERC721(owner(), beneficiary, address(tokenERC721));
    }

    /**
     * @notice Transfer ERC1155 tokens from owner to beneficiary.
     * @dev Callable by anybody
     */
    function releaseERC1155(
        IERC1155 tokenERC1155,
        uint[] calldata tokenIdList,
        uint[] calldata value
    ) external {
        require(
            block.timestamp >= releaseTime,
            "Current time is before release time"
        );
        require(
            tokenERC1155.isApprovedForAll(owner(), address(this)),
            "ERC1155 zero allowance"
        );
        tokenERC1155.safeBatchTransferFrom(
            owner(),
            beneficiary,
            tokenIdList,
            value,
            bytes("")
        );
        emit ReleasedERC1155(owner(), beneficiary, address(tokenERC1155));
    }

    function batchRelease(
        IERC20[] calldata tokenERC20List,
        IERC721[] calldata tokenERC721List,
        IERC1155[] calldata tokenERC1155List,
        uint[][] calldata ERC721tokenIdLists,
        uint[][] calldata ERC1155tokenIdLists,
        uint[][] calldata valueLists
    ) external {
        for (uint i = 0; i < tokenERC20List.length; i++) {
            this.releaseERC20(tokenERC20List[i]);
        }
        for (uint i = 0; i < tokenERC721List.length; i++) {
            this.releaseERC721(tokenERC721List[i], ERC721tokenIdLists[i]);
        }
        for (uint i = 0; i < tokenERC1155List.length; i++) {
            this.releaseERC1155(
                tokenERC1155List[i],
                ERC1155tokenIdLists[i],
                valueLists[i]
            );
        }
    }
}
