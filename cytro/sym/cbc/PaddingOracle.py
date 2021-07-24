import logging
import base64
import urllib.parse
from typing import Union, Callable
from concurrent.futures import ThreadPoolExecutor

__all__ = [
    'base64_encode', 'base64_decode',
    'urlencode', 'urldecode',
    'padding_oracle',
    'remove_padding', 'xor'
]

def xor(cipher, _from, _to):
    print("XOR", cipher, _from , _to)
    for target in [_from, _to] :
        if type(target) == int :
            cipher = xor_string(cipher,byte(target) * target)
        if  type(target) == bytes and len(target) == len(cipher):
            cipher = xor_string(cipher,target)
    return cipher

def _to_bytes(data: Union[str, bytes]):
    if isinstance(data, str):
        data = data.encode()
    assert isinstance(data, bytes)
    return data

def _to_str(data):
    if isinstance(data, bytes):
        data = data.decode()
    elif isinstance(data, str):
        pass
    else:
        data = str(data)
    return data

def base64_decode(data: Union[str, bytes]) -> bytes:
    data = _to_bytes(data)
    return base64.b64decode(data)

def base64_encode(data: Union[str, bytes]) -> str:
    data = _to_bytes(data)
    return base64.b64encode(data).decode()

def urlencode(data: Union[str, bytes]) -> str:
    data = _to_bytes(data)
    return urllib.parse.quote(data)

def urldecode(data: str) -> bytes:
    data = _to_str(data)
    return urllib.parse.unquote_plus(data)

def remove_padding(data: Union[str, bytes]):
    data = _to_bytes(data)
    return data[:-data[-1]]

def _dummy_oracle(cipher: bytes) -> bool:
    raise NotImplementedError('You must implement the oracle function')


def padding_oracle(cipher: bytes,
                   block_size: int,
                   oracle: Callable[[bytes], bool]=_dummy_oracle,
                   num_threads: int=1,
                   log_level: int=logging.INFO,
                   null: bytes=b' ') -> bytes:
    # Check the oracle function
    assert callable(oracle), 'the oracle function should be callable'
    assert oracle.__code__.co_argcount == 1, 'expect oracle function with only 1 argument'
    assert len(cipher) % block_size == 0, 'cipher length should be multiple of block size'
    
    logger = logging.getLogger('padding_oracle')
    logger.setLevel(log_level)
    formatter = logging.Formatter('[%(asctime)s][%(levelname)s] %(message)s')
    # formatter = logging.Formatter('[%(asctime)s][%(name)s][%(levelname)s] %(message)s')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # The plaintext bytes list to save the decrypted data
    plaintext = [null] * (len(cipher) - block_size)

    def _update_plaintext(i: int, c: bytes):
        plaintext[i] = c
        logger.info('plaintext: {}'.format(b''.join(plaintext)))

    oracle_executor = ThreadPoolExecutor(max_workers=num_threads)
    
    def _block_decrypt_task(i, prev: bytes, block: bytes):
        logger.debug('task={} prev={} block={}'.format(i, prev, block))
        guess_list = list(prev)
        
        for j in range(1, block_size + 1):
            oracle_hits = []
            oracle_futures = {}
            
            for k in range(256):
                if i == len(blocks) - 1 and j == 1 and k == prev[-j]:
                    # skip the last padding byte if it is identical to the original cipher
                    continue
                
                test_list = guess_list.copy()
                test_list[-j] = k
                oracle_futures[k] = oracle_executor.submit(oracle, bytes(test_list) + block)
            
            for k, future in oracle_futures.items():
                if future.result():
                    oracle_hits.append(k)
            
            logger.debug('oracles at block[{}][{}] -> {}'.format(i, block_size - j, oracle_hits))
                
            if len(oracle_hits) != 1:
                logfmt = 'at block[{}][{}]: expect only one positive result, got {}. (skipped)'
                logger.error(logfmt.format(i, block_size-j, len(oracle_hits)))
                return
            
            guess_list[-j] = oracle_hits[0]
            
            p = guess_list[-j] ^ j ^ prev[-j]
            _update_plaintext(i * block_size - j, bytes([p]))
            
            for n in range(j):
                guess_list[-n-1] ^= j
                guess_list[-n-1] ^= j + 1
    
    blocks = []
    
    for i in range(0, len(cipher), block_size):
        j = i + block_size
        blocks.append(cipher[i:j])
    
    logger.debug('blocks: {}'.format(blocks))
    
    with ThreadPoolExecutor() as executor:
        futures = []
        for i in reversed(range(1, len(blocks))):
            prev = b''.join(blocks[:i])
            block = b''.join(blocks[i:i+1])
            futures.append(executor.submit(_block_decrypt_task, i, prev, block))
        for future in futures:
            future.result()
    
    oracle_executor.shutdown()
    
    return b''.join(plaintext)