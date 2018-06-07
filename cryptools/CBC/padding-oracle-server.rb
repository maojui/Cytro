#!/usr/bin/ruby
require 'socket'
require 'openssl'
require 'base64'
require 'timeout'
require 'securerandom'

server = TCPServer.new 2000
$stdout.sync = true
Dir.chdir(File.dirname(__FILE__))

def encrypt_flag()
	flag = IO.binread('flag').strip()
	cipher = OpenSSL::Cipher::AES256.new(:CBC)
	cipher.encrypt
	cipher.key = IO.binread('key')
	cipher.iv = '8whXbWqehnACf6tZ'
	return Base64.strict_encode64(cipher.update(flag) + cipher.final)
end

def can_decrypt?(s)
	s = Base64.decode64(s)
	cipher = OpenSSL::Cipher::AES256.new(:CBC)
	cipher.decrypt
	cipher.key = IO.binread('key')
	cipher.iv = s.slice!(0...16)
	cipher.update(s)
	cipher.final
	true
	rescue OpenSSL::Cipher::CipherError
	false
end

def decrypt(s)
	s = Base64.decode64(s)
	cipher = OpenSSL::Cipher::AES256.new(:CBC)
	cipher.decrypt
	cipher.key = IO.binread('key')
	cipher.iv = s.slice!(0...16)
	return cipher.update(s)+cipher.final
	rescue OpenSSL::Cipher::CipherError
	false
end

while true  do
	begin
		client = server.accept
		client.puts 'Encrypted FLAG:'
		client.puts encrypt_flag()
		sleep(1)
		client.puts 'Can you decrypt it?'
		loop do
			s = client.gets
			client.puts can_decrypt?(s)
		end
	rescue
		
	end

end