import asyncio
from .Usuario import Usuario
from ...utils.firestore import add_data_with_id, delete_data, get_data, update_data, get_collection_data, increment, decrement, array_union

class UsuarioServicio:
    """
    Servicio para gestionar operaciones CRUD sobre usuarios en Firestore.
    """

    async def agregar_usuario(self, usuario: Usuario) -> None:
        """
        Agrega un nuevo usuario a la colección 'usuarios' en Firestore.

        Args:
            usuario (Usuario): Instancia de Usuario con los datos del usuario a agregar.

        Raises:
            ValueError: Si el ID del usuario es vacío.
        """
        usuario_id = usuario.get_id()
        
        if not usuario_id:
            raise ValueError("El ID del usuario no puede estar vacío")
        
        usuario_id = await add_data_with_id('usuarios', usuario.to_dict(), usuario_id)
        print(f'Usuario agregado con ID: {usuario_id}')

    async def eliminar_usuario(self, id: str) -> None:
        """
        Elimina un usuario de la colección 'usuarios' en Firestore.

        Args:
            id (str): ID del usuario a eliminar.
        """
        usuario_id = await delete_data('usuarios', id)
        print(f'Usuario eliminado con ID: {usuario_id}')

    async def actualizar_usuario(self, id: str, usuario_dict: dict) -> None:
        """
        Actualiza los datos de un usuario en la colección 'usuarios' en Firestore.

        Args:
            id (str): ID del usuario a actualizar.
            usuario_dict (dict): Diccionario con los datos a actualizar.

        Raises:
            ValueError: Si se intenta actualizar el ID, saldo, total_apostado o historial del usuario.
        """
        if not "id" in usuario_dict and not "saldo" in usuario_dict and not "total_apostado" in usuario_dict and not "historial" in usuario_dict:
            usuario_id = await update_data('usuarios', id, usuario_dict)
            print(f'Usuario actualizado con ID: {usuario_id}')
        else:
            raise ValueError("No se puede actualizar el ID, saldo, total_apostado o historial del usuario")

    async def obtener_usuario(self, id: str) -> Usuario:
        """
        Obtiene un usuario de la colección 'usuarios' en Firestore.

        Args:
            id (str): ID del usuario a obtener.

        Returns:
            Usuario: Instancia de Usuario con los datos obtenidos.
        """
        usuario_dict = await get_data('usuarios', id)
        if usuario_dict is None:
            raise ValueError(f"No se encontró usuario con ID: {id}")
        usuario = Usuario.from_dict(usuario_dict)
        return usuario

    @staticmethod
    async def obtener_todos_usuarios() -> list[Usuario]:
        """
        Obtiene todos los usuarios de la colección 'usuarios' en Firestore.

        Returns:
            list[Usuario]: Lista de instancias de Usuario.
        """
        usuarios_dict = await get_collection_data('usuarios')
        usuarios = [Usuario.from_dict(usuario_dict) for usuario_dict in usuarios_dict if usuario_dict is not None]
        return usuarios
    
    async def aumentar_saldo(self, id: str, monto: float) -> None:
        """
        Sube el saldo de un usuario en Firestore.

        Args:
            id (str): ID del usuario.
            monto (float): Monto a sumar al saldo del usuario.

        Raises:
            ValueError: Monto debe ser mayor a 0.
        """
        if monto > 0:
            usuario_id = await update_data('usuarios', id, {'saldo': increment(monto)})
            print(f'Saldo actualizado con ID: {usuario_id}')
        else:
            raise ValueError("Monto debe ser mayor a 0")
        
    async def disminuir_saldo(self, id: str, monto: float) -> None:
        """
        Baja el saldo de un usuario en Firestore.

        Args:
            id (str): ID del usuario.
            monto (float): Monto a restar al saldo del usuario.

        Raises:
            ValueError: Monto debe ser mayor a 0.
        """
        if monto > 0:
            usuario_id = await update_data('usuarios', id, {'saldo': decrement(monto)})
            print(f'Saldo actualizado con ID: {usuario_id}')
        else:
            raise ValueError("Monto debe ser mayor a 0")
        
    async def incrementar_total_apostado(self, id: str, monto: float) -> None:
        """
        Incrementa el total apostado de un usuario en Firestore.

        Args:
            id (str): ID del usuario.
            monto (float): Monto a incrementar en el total apostado del usuario.

        Raises:
            ValueError: Monto debe ser mayor a 0.
        """
        if monto > 0:
            usuario_id = await update_data('usuarios', id, {'total_apostado': increment(monto)})
            print(f'Total apostado actualizado con ID: {usuario_id}')
        else:
            raise ValueError("Monto debe ser mayor a 0")
        
    async def agregar_historial(self, id: str, historial: dict) -> None:
        """
        Agrega un historial de apuestas a un usuario en Firestore.

        Args:
            id (str): ID del usuario.
            historial (dict): Diccionario de historiales de apuestas a agregar.
        """
        
        usuario_id = await update_data('usuarios', id, {'historial': array_union([historial])})
        print(f'historial actualizado del usuario: {usuario_id}')

    async def buscar_usuario_por_correo(self, correo: str) -> Usuario | None:
        """
        Busca un usuario por su correo electrónico en Firestore.

        Args:
            correo (str): Correo electrónico del usuario a buscar.

        Returns:
            Usuario | None: Instancia de Usuario si se encuentra, None si no existe.
        """
        try:
            usuarios_dict = await get_collection_data('usuarios')
            for usuario_dict in usuarios_dict:
                if usuario_dict.get('correo') == correo:
                    return Usuario.from_dict(usuario_dict)
            return None
        except Exception as e:
            print(f"Error al buscar usuario por correo: {e}")
            return None

    async def autenticar_usuario(self, correo: str, contraseña: str) -> dict:
        """
        Autentica un usuario verificando correo y contraseña.

        Args:
            correo (str): Correo electrónico del usuario.
            contraseña (str): Contraseña del usuario.

        Returns:
            dict: Diccionario con el resultado de la autenticación.
                - success (bool): True si la autenticación es exitosa.
                - message (str): Mensaje descriptivo del resultado.
                - user (Usuario | None): Instancia del usuario si la autenticación es exitosa.
        """
        try:
            # Buscar usuario por correo
            usuario = await self.buscar_usuario_por_correo(correo)
            
            if usuario is None:
                return {
                    'success': False,
                    'message': 'Correo no registrado',
                    'user': None
                }
            
            # Verificar contraseña
            if usuario.get_contraseña() == contraseña:
                return {
                    'success': True,
                    'message': 'Inicio de sesión exitoso',
                    'user': usuario
                }
            else:
                return {
                    'success': False,
                    'message': 'Contraseña incorrecta',
                    'user': None
                }
                
        except Exception as e:
            return {
                'success': False,
                'message': f'Error en la autenticación: {str(e)}',
                'user': None
            }
        
async def main():
    usuario_servicio = UsuarioServicio()
    usuario = Usuario.crear_usuario("Miguel Angel", "Ospina Giraldo", 1000)
    await usuario_servicio.actualizar_usuario("MO317", {"nombre" : "Miguel Jose"})

    # Agregar un usuario
    
if __name__ == "__main__":
    asyncio.run(main())
    print('hola')
