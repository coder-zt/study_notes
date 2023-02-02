

import javax.crypto.Cipher;
import java.security.KeyPair;
import java.security.KeyPairGenerator;
import java.security.PrivateKey;
import java.security.PublicKey;

/**
 * @author xietansheng
 */
public class gsonDemo {

    public static void main(String[] args) throws Exception {
        // 随机生成一对密钥（包含公钥和私钥）
        KeyPair keyPair = generateKeyPair();
        // 获取 公钥 和 私钥
        PublicKey pubKey = keyPair.getPublic();
        PrivateKey priKey = keyPair.getPrivate();

        // 原文数据
        String data = "你好, World!";

        // 客户端: 用公钥加密原文, 返回加密后的数据
        byte[] cipherData = encrypt(data.getBytes(), pubKey);

        // 服务端: 用私钥解密数据, 返回原文
        byte[] plainData = decrypt(cipherData, priKey);

        // 输出查看解密后的原文
        System.out.println(new String(plainData));  // 结果打印: 你好, World!
    }

    /**
     * 随机生成密钥对（包含公钥和私钥）
     */
    private static KeyPair generateKeyPair() throws Exception {
        // 获取指定算法的密钥对生成器
        KeyPairGenerator gen = KeyPairGenerator.getInstance("RSA");

        // 初始化密钥对生成器（密钥长度要适中, 太短不安全, 太长加密/解密速度慢）
        gen.initialize(2048);

        // 随机生成一对密钥（包含公钥和私钥）
        return gen.generateKeyPair();
    }

    /**
     * 公钥加密数据
     */
    private static byte[] encrypt(byte[] plainData, PublicKey pubKey) throws Exception {
        // 获取指定算法的密码器
        Cipher cipher = Cipher.getInstance("RSA");

        // 初始化密码器（公钥加密模型）
        cipher.init(Cipher.ENCRYPT_MODE, pubKey);

        // 加密数据, 返回加密后的密文
        return cipher.doFinal(plainData);
    }

    /**
     * 私钥解密数据
     */
    private static byte[] decrypt(byte[] cipherData, PrivateKey priKey) throws Exception {
        // 获取指定算法的密码器
        Cipher cipher = Cipher.getInstance("RSA");

        // 初始化密码器（私钥解密模型）
        cipher.init(Cipher.DECRYPT_MODE, priKey);

        // 解密数据, 返回解密后的明文
        return cipher.doFinal(cipherData);
    }

}
