// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract CertificateRegistry {
    
    address public owner;

    constructor() {
        owner = msg.sender;
    }

    struct Certificate {
        string name;
        string code;
        string eventname;
        string eventdate;
        string issuedBy;
        address issuer;
        uint256 timestamp;
    }

    mapping(string => Certificate) private certificates;
    mapping(string => bool) private codeExists;

    event CertificateIssued(
        string code,
        string name,
        string eventname,
        string eventdate,
        string issuedBy,
        address issuer,
        uint256 timestamp
    );

    modifier onlyOwner() {
        require(msg.sender == owner, "Not authorized");
        _;
    }

    function issueCertificate(
        string memory _name,
        string memory _code,
        string memory _eventname,
        string memory _eventdate,
        string memory _issuedBy
    ) public onlyOwner {
        require(!codeExists[_code], "Code already used");

        certificates[_code] = Certificate({
            name: _name,
            code: _code,
            eventname: _eventname,
            eventdate: _eventdate,
            issuedBy: _issuedBy,
            issuer: msg.sender,
            timestamp: block.timestamp
        });

        codeExists[_code] = true;

        emit CertificateIssued(
            _code,
            _name,
            _eventname,
            _eventdate,
            _issuedBy,
            msg.sender,
            block.timestamp
        );
    }

    function verifyCertificate(string memory _code)
        public
        view
        returns (
            string memory name,
            string memory code,
            string memory eventname,
            string memory eventdate,
            string memory issuedBy,
            address issuer,
            uint256 timestamp,
            bool valid
        )
    {
        if (!codeExists[_code]) {
            return ("", "", "", "", "", address(0), 0, false);
        }

        Certificate memory cert = certificates[_code];
        return (
            cert.name,
            cert.code,
            cert.eventname,
            cert.eventdate,
            cert.issuedBy,
            cert.issuer,
            cert.timestamp,
            true
        );
    }
}