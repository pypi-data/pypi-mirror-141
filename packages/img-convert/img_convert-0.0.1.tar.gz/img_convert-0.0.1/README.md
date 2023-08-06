# img-convert

Este pacote é usado para converter uma imagem RGB para Pecil Sketch.
	
## Instalação

Use o gerenciador de pacotes [pip](https://pip.pypa.io/en/stable/) para instalar este pacote.

```bash
pip install img_convert
```

## Uso

```python
from img_convert.utils.io import ConvertImg
image_path = ''

img = ConvertImg()
img.to_pencil_sketch(image_path)
```

## Autor
Thiago Oliveira

## License
[MIT](https://choosealicense.com/licenses/mit/)