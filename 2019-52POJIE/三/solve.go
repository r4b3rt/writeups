package main

import (
    "fmt"
    "bytes"
    "crypto/cipher"
    "crypto/sha1"
    "crypto/aes"
    "encoding/base64"
)

func PKCS5Padding(ciphertext []byte, blockSize int) []byte {
    padding := blockSize - len(ciphertext)%blockSize
    padtext := bytes.Repeat([]byte{byte(padding)}, padding)
    return append(ciphertext, padtext...)
}

func PKCS5UnPadding(origData []byte) []byte {
    length := len(origData)
    unpadding := int(origData[length-1])
    return origData[:(length - unpadding)]
}

func AesEncrypt(origData, key []byte) ([]byte, error) {
    block, err := aes.NewCipher(key)
    if err != nil {
        return nil, err
    }
    blockSize := block.BlockSize()
    origData = PKCS5Padding(origData, blockSize)
    blockMode := cipher.NewCBCEncrypter(block, key[:blockSize])
    crypted := make([]byte, len(origData))
    blockMode.CryptBlocks(crypted, origData)
    return crypted, nil
}

func AesDecrypt(crypted, key []byte) ([]byte, error) {
    block, err := aes.NewCipher(key)
    if err != nil {
        return nil, err
    }
    blockSize := block.BlockSize()
    blockMode := cipher.NewCBCDecrypter(block, key[:blockSize])
    origData := make([]byte, len(crypted))
    blockMode.CryptBlocks(origData, crypted)
    origData = PKCS5UnPadding(origData)
    return origData, nil
}

func main() {
    uid := "975446"
    h := sha1.New()
    h.Write([]byte(uid))
    bs := h.Sum(nil)
    var aeskey = bs[0:16]
	fmt.Println("AES Key: ", aeskey)
    pass := []byte("HappyNewYearFrom52PoJie.Cn")
    xpass, err := AesEncrypt(pass, aeskey)
    if err != nil {
        fmt.Println(err)
        return
    }
    pass64 := base64.StdEncoding.EncodeToString(xpass)
    fmt.Printf("Ciphertext: %v\n",pass64)
    bytesPass, err := base64.StdEncoding.DecodeString(pass64)
    if err != nil {
        fmt.Println(err)
        return
    }
    tpass, err := AesDecrypt(bytesPass, aeskey)
    if err != nil {
        fmt.Println(err)
        return
    }
    fmt.Printf("Plaintext: %s\n", tpass)
}
