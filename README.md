# jellyfin-hwcodec-tabulator
## Usage: 
```sh 
python jellyfin_hwcodec.py --device renderD128
```  
renderD128 is usually the iGPU and renderD129 a dedicated GPU.  
Check `ls /dev/dri/` for available VA-API devices.  
