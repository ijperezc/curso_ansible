
from awx_module import conectar_awx, crear_proyecto, crear_plantilla


def main():
    session_conn = conectar_awx()
    #session_conn = conectar_awx('http://127.0.0.1:40167/','admin','VtdeKzqfjICwJR3ptfO1pqeOqMwnfheQ')
    if session_conn:

        # Crear proyecto
        #proyecto = crear_proyecto(session_conn, 'proyecto4', 'https://github.com/ijperezc/curso_ansible.git')
        #print(proyecto)

        # obtener proyecto
        proyecto = session_conn.projects.get(name='proyecto3').results[0]

        #  obtener inventario
        inventario = session_conn.inventory.get(name='linux_inventory').results[0]

        # obtener credenciales (linux + vault)
        credencial_linux = session_conn.credentials.get(name='linux_credential').results[0]
        credencial_vault = session_conn.credentials.get(name='vault').results[0]

        template = crear_plantilla(session_conn, "DemoJob14", proyecto.id, inventario.id, [credencial_linux.id, credencial_vault.id], 'playbook5.yml')

        if template:
            print(template)
            # Ejecutar job
            #launch_job = job_templates.JobTemplate.launch(template)
            #job_templates.JobTemplate.wait_until_status(launch_job, status="successful", timeout=30)
        else:
            print("La plantilla no se ha creado")
        
        #job3 = session_conn.job_templates.get(id=14).results[0]
        #print("Info job2:", job3)

        # ejecutar job
        #launch_job = job_templates.JobTemplate.launch(job3)

        # esperar a que acabe el job
        #job_templates.JobTemplate.wait_until_status(launch_job, status="successful", timeout=20)


if __name__ == "__main__":
    main()