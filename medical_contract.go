package main

import (
	"fmt"
	"log"
	"github.com/hyperledger/fabric-contract-api-go/contractapi"
)

type MedicalContract struct {
	contractapi.Contract
}

func (s *MedicalContract) StoreImageHash(ctx contractapi.TransactionContextInterface, imageID string, hash string) error {
	return ctx.GetStub().PutState(imageID, []byte(hash))
}

func (s *MedicalContract) QueryImageHash(ctx contractapi.TransactionContextInterface, imageID string) (string, error) {
	hashBytes, err := ctx.GetStub().GetState(imageID)
	if err != nil || hashBytes == nil {
		return "", fmt.Errorf("image not found")
	}
	return string(hashBytes), nil
}

func main() {
	medicalChaincode, err := contractapi.NewChaincode(&MedicalContract{})
	if err != nil {
		log.Panicf("Error creating medical chaincode: %v", err)
	}
	if err := medicalChaincode.Start(); err != nil {
		log.Panicf("Error starting medical chaincode: %v", err)
	}
}
