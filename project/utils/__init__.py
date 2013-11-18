from slughifi import slughifi

def borrar_fotos_anteriores_usuario(usuario):
	try:
		from django.conf import settings
		import os
		media = settings.MEDIA_ROOT
		media_usuario = os.path.join(media, "FotosPerfil/%s" % usuario)
		archivos_o_es_vacio = os.listdir(media_usuario)
		if archivos_o_es_vacio:
			for archivo in archivos_o_es_vacio:
				os.unlink(os.path.join(media_usuario,archivo))
	except Exception as e:
		pass

def ver_si_existe(archivo):
	try:
		from django.conf import settings
		import os
		media = settings.MEDIA_ROOT
		media_fotos = os.path.join(media, "FotosPosts")
		foto = os.path.join(media_fotos, archivo)
		if os.path.exists(foto):
			os.unlink(foto)
			return "FotosPosts/%s" % archivo
		else:
			return False
	except Exception as e:
		return False
