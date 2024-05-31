package main

import (
    "fmt"
    "github.com/hyperledger/fabric-contract-api-go/contractapi"
)

type SmartContract struct {
    contractapi.Contract
}

func (s *SmartContract) StoreDocument(ctx contractapi.TransactionContextInterface, key string, documentHash string) error {
    return ctx.GetStub().PutState(key, []byte(documentHash))
}

func (s *SmartContract) RetrieveDocument(ctx contractapi.TransactionContextInterface, key string) (string, error) {
    documentHash, err := ctx.GetStub().GetState(key)
    if err != nil {
        return "", err
    }
    if documentHash == nil {
        return "", fmt.Errorf("document not found")
    }
    return string(documentHash), nil
}

func main() {
    chaincode, err := contractapi.NewChaincode(&SmartContract{})
    if err != nil {
        fmt.Printf("Error create chaincode: %s", err.Error())
        return
    }

    if err := chaincode.Start(); err != nil {
        fmt.Printf("Error starting chaincode: %s", err.Error())
    }
}
