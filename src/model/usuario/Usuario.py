"""
Módulo que define la clase Usuario del Casino
"""


from ...utils.Util import generador_random


class Usuario:
    """
    Clase que representa un usuario del casino

    Attributes:
        _id (str): Identificador único del usuario
        _nombre (str): Nombre del usuario
        _apellido (str): Apellido del usuario
        _saldo (float): Saldo actual del usuario
        _total_apostado (float): Total de dinero apostado por el usuario
        _historial (list): Historial de transacciones del usuario
    """

    _id: str
    _nombre: str
    _apellido: str
    _saldo: float
    _total_apostado: float
    _correo: str
    _contraseña: str
    _historial: list
    _vip: bool
    _ciudad: str

    def __init__(
        self,
        id: str,
        nombre: str,
        apellido: str,
        correo: str,
        contraseña: str,
        saldo: float = 0.0,
        total_apostado: float = 0.0,
        historial: list = [],
        vip: bool = False,
        ciudad:str = 'Ciudad no especificada'
    ) -> None:
        """
        Inicializa un nuevo usuario

        Args:
            id (str): Identificador único del usuario
            nombre (str): Nombre del usuario
            apellido (str): Apellido del usuario
            saldo (float, optional): Saldo inicial. Por defecto 0.0
            total_apostado (float, optional): Total apostado inicial. Por defecto 0.0
            historial (list, optional): Historial de transacciones. Por defecto []

        """
        self.set_nombre(nombre)
        self.set_apellido(apellido)
        self.set_correo(correo)
        self.set_contraseña(contraseña)
        self.set_id(id)
        self.set_vip(vip) 
        self.set_saldo(saldo)
        self.set_total_apostado(total_apostado)
        self.__set_historial(historial)
        
    @classmethod
    async def crear_usuario(cls, nombre: str, apellido: str, correo: str, contraseña: str) -> 'Usuario':
        from .UsuarioServicio import UsuarioServicio
        """
        Inicializa un nuevo usuario           
        Args:
            nombre (str): Nombre del usuario
            apellido (str): Apellido del usuario
            correo (str): Correo del usuario
            contraseña (str): Contraseña del usuario
        """
        servicio = UsuarioServicio()
        id = ""  # Generate or assign an ID as needed
        total_apostado = 0.0
        historial = []
        saldo = 1000.0
        vip = False  # Default VIP status is False
        user = cls(id, nombre, apellido, correo, contraseña, saldo, total_apostado, historial, vip)
        await servicio.agregar_usuario(user)
        return user
    
    @classmethod
    def crear_usuario_local(cls, nombre: str, apellido: str) -> 'Usuario':
        """
        Crea un usuario local sin conexión a la base de datos

        Args:
            nombre (str): Nombre del usuario
            apellido (str): Apellido del usuario

        Returns:
            Usuario: Nueva instancia de Usuario
        """
        id = ""
        correo = "x@x.com"
        contraseña = "xxxx"
        saldo = 1000.0
        total_apostado = 0.0
        historial = []
        return cls(id, nombre, apellido, correo, contraseña, saldo, total_apostado, historial, vip=False)
        

    @classmethod
    def from_dict(cls, data: dict):
        """
        Crea una instancia de Usuario a partir de un diccionario

        Args:
            data (dict): Diccionario con los datos del usuario

        Returns:
            Usuario: Nueva instancia de Usuario
        """
        print(data)
        id = data.get('id', '')
        nombre = data.get('nombre', '')
        apellido = data.get('apellido', '')
        saldo = data.get('saldo', 0.0)
        vip = data.get('vip', False)
        total_apostado = data.get('total_apostado', 0.0)
        correo = data.get('correo', '')
        contraseña = data.get('contraseña', '')
        historial = data.get('historial', [])
        

        return cls(id, nombre, apellido, correo, contraseña, saldo, total_apostado, historial, vip)

    def get_id(self) -> str:
        """Retorna el ID del usuario"""
        return self._id

    def get_nombre(self) -> str:
        """Retorna el nombre del usuario"""
        return self._nombre

    def get_apellido(self) -> str:
        """Retorna el apellido del usuario"""
        return self._apellido

    def get_saldo(self) -> float:
        """Retorna el saldo actual del usuario"""
        return self._saldo

    def get_total_apostado(self) -> float:
        """Retorna el total apostado por el usuario"""
        return self._total_apostado
    
    def get_correo(self) -> str:
        """Retorna el correo del usuario"""
        return self._correo
    
    def get_contraseña(self) -> str:
        """Retorna la contraseña del usuario"""
        return self._contraseña

    def get_historial(self) -> list:
        """Retorna el historial de transacciones del usuario"""
        return self._historial

    def generar_id(self) -> str:
        """
        Genera un ID único para el usuario usando las iniciales y un número aleatorio
        """
        num_random = generador_random(100, 999)
        return (
            f"{self._nombre[0].upper()}{self._apellido[0].upper()}{num_random}"
        )

    def set_id(self, id: str) -> None:
        """
        Establece el ID del usuario

        Args:
            id (str): Nuevo ID

        Raises:
            ValueError: Si el ID es inválido
        """
        if id == "":
            self._id = self.generar_id()
        else:
            self._id = id   

    def set_nombre(self, nombre: str) -> None:
        """
        Establece el nombre del usuario

        Args:
            nombre (str): Nuevo nombre

        Raises:
            ValueError: Si el nombre es inválido
        """
        if not nombre == "" and not (nombre is None) and (len(nombre) > 3) and (len(nombre) < 30):
            self._nombre = nombre
        else:
            raise ValueError(
                "El nombre no puede ser vacío o None y debe tener entre 3 y 30 caracteres"
            )

    def set_apellido(self, apellido: str) -> None:
        """
        Establece el apellido del usuario

        Args:
            apellido (str): Nuevo apellido

        Raises:
            ValueError: Si el apellido es inválido
        """
        if not ( apellido == "") and not (apellido is None) and (len(apellido) > 3) and (len(apellido) < 30):
            self._apellido = apellido
        else:
            raise ValueError(
                "El apellido no puede ser vacío o None y debe tener entre 3 y 30 caracteres"
            )
            
    def set_vip(self, vip: bool) -> None:
        """
        Establece el estado VIP del usuario

        Args:
            vip (bool): Estado VIP del usuario
        """
        self._vip = vip

    def set_saldo(self, saldo: float) -> None:
        """
        Establece el saldo del usuario

        Args:
            saldo (float): Nuevo saldo

        Raises:
            ValueError: Si el saldo es negativo
        """
        if not saldo < 0:
            self._saldo = saldo
            if self._saldo >= 1000:
                self.set_vip(True)
            else:
                self.set_vip(False)
        else:
            raise ValueError("El saldo no puede ser negativo")

    def set_total_apostado(self, total_apostado: float) -> None:
        """
        Establece el total apostado por el usuario

        Args:
            total_apostado (float): Nuevo total apostado

        Raises:
            ValueError: Si el total apostado es negativo
        """
        if not total_apostado < 0:
            self._total_apostado = total_apostado
        else:
            raise ValueError("El total apostado no puede ser negativo")
        
    def set_correo(self, correo: str) -> None:
        """
        Establece el correo del usuario

        Args:
            correo (str): Nuevo correo

        Raises:
            ValueError: Si el correo es inválido
        """
        if "@" in correo and "." in correo:
            self._correo = correo
        else:
            raise ValueError("El correo debe contener '@' y '.'")
    def set_contraseña(self, contraseña: str) -> None:
        """
        Establece la contraseña del usuario

        Args:
            contraseña (str): Nueva contraseña

        Raises:
            ValueError: Si la contraseña es inválida
        """
        if len(contraseña) >= 3:
            self._contraseña = contraseña
        else:
            raise ValueError("La contraseña debe tener al menos 3 caracteres")

    def __set_historial(self, historial: list) -> None:
        """
        Establece el historial de transacciones

        Args:
            historial (list): Nueva lista de historial
        """
        self._historial = historial

    async def agregar_historial(self, registro: dict) -> None:
        from .UsuarioServicio import UsuarioServicio
        servicio = UsuarioServicio()
        """
        Agrega un nuevo registro al historial

        Args:
            registro (list): Registro a agregar
        """
        self._historial.append(registro)
        await servicio.agregar_historial(self._id, registro)

    async def aumentar_saldo(self, monto: float) -> None:
        from .UsuarioServicio import UsuarioServicio
        servicio = UsuarioServicio()
        
        """
        Aumenta el saldo del usuario

        Args:
            monto (float): Cantidad a aumentar

        Raises:
            ValueError: Si el monto es negativo o cero
        """
        if monto > 0:
            self._saldo += monto
            await servicio.aumentar_saldo(self._id, monto)
        else:
            raise ValueError("El monto a aumentar debe ser positivo")


    def get_ciudad(self) -> str:
        """
        Retorna la ciudad del usuario
        """
        if self._ciudad is None or self._ciudad == "":
            return "Ciudad no especificada"

        return self._ciudad

    async def disminuir_saldo(self, monto: float) -> None:
        from .UsuarioServicio import UsuarioServicio
        servicio = UsuarioServicio()
        """
        Disminuye el saldo del usuario

        Args:
            monto (float): Cantidad a disminuir

        Raises:
            ValueError: Si el monto es negativo, cero o mayor al saldo actual
        """
        if monto > 0 or monto < self._saldo:
            self._saldo -= monto
            await servicio.disminuir_saldo(self._id, monto)
        else:    
            raise ValueError(
                "El monto a disminuir debe ser positivo y no puede ser mayor al saldo actual"
            )
            
    async def incrementar_total_apostado(self, monto: float) -> None:
        from .UsuarioServicio import UsuarioServicio
        servicio = UsuarioServicio()
        """
        Aumenta el total apostado del usuario

        Args:
            monto (float): Cantidad a aumentar

        Raises:
            ValueError: Si el monto es negativo o cero
        """
        if monto > 0:
            self._total_apostado += monto
            await servicio.incrementar_total_apostado(self._id, monto)
        else:
            raise ValueError("El monto a aumentar debe ser positivo")
        
    def to_dict(self) -> dict:
        """
        Convierte el objeto Usuario en un diccionario

        Returns:
            dict: Diccionario con los atributos del objeto Usuario
        """
        return {
            "id": self._id,
            "nombre": self._nombre,
            "apellido": self._apellido,
            "saldo": self._saldo,
            "total_apostado": self._total_apostado,
            "correo": self._correo,
            "contraseña": self._contraseña,
            "historial": self._historial,
            "vip": self._vip
        }

    def __repr__(self):
        return (
            f"id: {self._id}\n"
            f"nombre: {self._nombre}\n"
            f"apellido: {self._apellido}\n"
            f"saldo: {self._saldo}\n"
            f"total_apostado: {self._total_apostado}\n"
            f"correo: {self._correo}\n"
            f"contraseña: {self._contraseña}\n"
            f"historial: {self._historial}\n"
            f"vip: {self._vip}\n"
        )
