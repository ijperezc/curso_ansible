from awxkit import config, utils
from awxkit.api import ApiV2, job_templates
from awxkit.api.resources import resources
import os


def conectar_awx(url: str = None, usuario: str = None, password: str = None):
    """"""
    try:
        config.base_url = url or os.environ.get('AWX_URL') # Obtiene la url que le pasemos al invocar la función o en caso contrario la captura de las variables del entorno
        config.credentials = utils.PseudoNamespace(
            {
                'default': {
                    'username': usuario or os.environ.get('AWX_USERNAME'),
                    'password': password or os.environ.get('AWX_PASSWORD')
                }
            }
        )
        session_conn = ApiV2().load_session().get() # Invoca a ApiV2 para obtener la conexión
        session_conn.get(resources) # abre la conexión pasando los recursos url y credentials

        return session_conn # devuelve la conexión creada
    except Exception as ex:
        print(ex)
        return None
    
def crear_proyecto(client, nombre: str, url_git: str, branch: str = 'main'):

    try:
        # obtener la organizacion (Default)
        organizacion = client.organizations.get(name='Default').results[0]
        #print(organizacion)

        proyecto = client.projects.post({
            'name': nombre,
            'description': f"Proyecto {nombre}",
            'scm_type': 'git',
            'scm_url': url_git,
            'scm_branch': branch,
            'organization': organizacion.id
        })

        print(f"Proyecto creado.")
        return proyecto

    except Exception as ex:
        print(ex)
        return None
    
def crear_plantilla(client, nombre: str, proyecto_id: int, inventario_id: int, lista_credenciales: list, playbook: str):

    try:
        template = client.job_templates.post(
                {
                    'name': nombre,
                    'description': f"Template {nombre}",
                    'job_type': 'run',
                    'inventory': inventario_id,
                    'project': proyecto_id,
                    'playbook': playbook,
                    #'credential': credencial_id,
                    'become_enabled': True
                }
        )
        
        # añadir credencial a la template (mas alla de establecer su id)

        for credencial_id in  lista_credenciales:
            credencial = client.credentials.get(id=credencial_id).results[0]
            job_templates.JobTemplate.add_credential(template, credencial)


        
        print('Template creada.')
        return template
     
    except Exception as ex:
        print(ex)
        return None