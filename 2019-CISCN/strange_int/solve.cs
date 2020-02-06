using System;
 
namespace Solve {
	class Program {
		public static byte[] intToBytes(uint value) {
			byte[] res = new byte[4];
			res[3] = (byte) ((value >> 24) & 0xFF);
			res[2] = (byte) ((value >> 16) & 0xFF);
			res[1] = (byte) ((value >> 8) & 0xFF);
			res[0] = (byte) (value & 0xFF);
			return res;
		}

		public static string asciiToString(byte[] array) {
			return Convert.ToString(System.Text.Encoding.ASCII.GetString(array));
		}

		static void Main(string[] args) {
			var data = new uint[] {
				0x61646238, 0x36353465, 0x6361352d, 0x31312d38, 0x612d3965, 0x2d316331, 0x39653838, 0x30386566, 0x66616566, 0x57635565, 0x06530401, 0x1f494949, 0x5157071f, 0x575f4357, 0x57435e57, 0x4357020a, 0x575e035e, 0x0f590000, 0x6e6f7277, 0x20202067, 0x00202020, 0x72726f63, 0x20746365, 0x20202020, 0x6c660020, 0x69206761, 0x6c662073, 0x597b6761, 0x5072756f, 0x68637461, 0x2020207d, 0x20202020, 0x20202020, 0x20202020, 0x20202020, 0x20202020, 0x20202020, 0xffffff00, 0xffffffff
			};
			var ans = new uint[data.Length];
			var patch = new byte[data.Length * 4];
			for(uint i = 0; i < 9; i++) {
				uint t = 0;
				for(uint j = 0; j <= 0x7FFFFFFF; j++) {
					t = j ^ (j << 8) ^ (j << 16) ^ (j << 24);
					if(i > 0) {
						t ^= ans[i - 1] ^ (ans[i - 1] << 8) ^ (ans[i - 1] << 16) ^ (ans[i - 1] << 24);
					}
					if(t == data[i + 9]) { // 0x57635565
						ans[i] = j;
						patch[4 * i] = intToBytes(j)[0];
						patch[4 * i + 1] = intToBytes(j)[1];
						patch[4 * i + 2] = intToBytes(j)[2];
						patch[4 * i + 3] = intToBytes(j)[3];
						Console.WriteLine("0x{0:X8}", j);
						break;
					}
				}
			}
			string flag = asciiToString(patch);
			Console.WriteLine(flag);
		}
	}
}
