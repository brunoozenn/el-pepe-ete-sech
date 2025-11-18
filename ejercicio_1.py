from abc import ABC, abstractmethod

# ============================
# CLASE ABSTRACTA VEHICULO
# ============================
class Vehiculo(ABC):
    def __init__(self, id_vehiculo, capacidad_tn, estado="Disponible"):
        self._id_vehiculo = id_vehiculo
        self._capacidad_tn = None
        self.capacidad_tn = capacidad_tn   # usa la property para validar
        self._estado = estado

    # Getter (propiedad pública)
    @property
    def capacidad_tn(self):
        return self._capacidad_tn

    # Setter validado
    @capacidad_tn.setter
    def capacidad_tn(self, valor):
        if valor < 0:
            raise ValueError("Capacidad no puede ser negativa")
        self._capacidad_tn = valor

    @property
    def id_vehiculo(self):
        return self._id_vehiculo

    @property
    def estado(self):
        return self._estado

    def cambiar_estado(self, nuevo):
        self._estado = nuevo

    @abstractmethod
    def calcular_rendimiento(self, distancia, peso):
        pass


# ============================
# SUBCLASES DE VEHICULO
# ============================
class CamionTolva(Vehiculo):
    def __init__(self, id_vehiculo, capacidad_tn, resistencia_chasis):
        super().__init__(id_vehiculo, capacidad_tn)
        self.resistencia_chasis = resistencia_chasis

    def calcular_rendimiento(self, distancia, peso):
        # ejemplo: rendimiento relativo a carga y resistencia
        carga_frac = min(peso / self.capacidad_tn, 1.0)
        rendimiento = (1 / (1 + carga_frac)) * distancia * (self.resistencia_chasis / 100)
        return round(rendimiento, 3)


class VolqueteArticulado(Vehiculo):
    def __init__(self, id_vehiculo, capacidad_tn, num_ejes):
        super().__init__(id_vehiculo, capacidad_tn)
        self.num_ejes = num_ejes

    def calcular_rendimiento(self, distancia, peso):
        factor_ejes = 1 + (self.num_ejes - 2) * 0.05
        carga_frac = min(peso / self.capacidad_tn, 1.0)
        rendimiento = distancia * factor_ejes * (1 - 0.2 * carga_frac)
        return round(rendimiento, 3)


class CamionLigero(Vehiculo):
    def __init__(self, id_vehiculo, capacidad_tn, tipo_suspension):
        super().__init__(id_vehiculo, capacidad_tn)
        self.tipo_suspension = tipo_suspension

    def calcular_rendimiento(self, distancia, peso):
        carga_frac = min(peso / self.capacidad_tn, 1.0)
        base = distancia * 0.6
        penalizacion = carga_frac * 0.8 * distancia
        rendimiento = base - penalizacion
        if rendimiento < 0:
            rendimiento = 0
        return round(rendimiento, 3)


# ============================
# CLASE ABSTRACTA OPERADOR
# ============================
class Operador(ABC):
    def __init__(self, nombre, dni, licencia):
        self._nombre = nombre
        self._dni = dni
        self._licencia = licencia
        self.vehiculos_asociados = []

    @property
    def nombre(self):
        return self._nombre

    def asociar_vehiculo(self, vehiculo):
        if vehiculo not in self.vehiculos_asociados:
            self.vehiculos_asociados.append(vehiculo)

    @abstractmethod
    def registrar_operacion(self, operacion):
        pass

    @abstractmethod
    def calcular_bonos(self):
        pass


# ============================
# SUBTIPOS DE OPERADOR
# ============================
class OperadorCamion(Operador):
    def registrar_operacion(self, operacion):
        print("OperadorCamion registró la operación", operacion.id_op)

    def calcular_bonos(self):
        return 100


class SupervisorTransporte(Operador):
    def registrar_operacion(self, operacion):
        print("Supervisor validó la operación", operacion.id_op)

    def calcular_bonos(self):
        return 200


class ControladorAlmacen(Operador):
    def registrar_operacion(self, operacion):
        print("Controlador registró el ingreso de la operación", operacion.id_op)

    def calcular_bonos(self):
        return 80


# ============================
# COMPOSICIÓN: CARGA MINERAL
# ============================
class CargaMineral:
    def __init__(self, tipo, humedad, peso):
        self.tipo = tipo
        self.humedad = humedad
        self._peso = None
        self.peso = peso   # usa setter para validar

    @property
    def peso(self):
        return self._peso

    @peso.setter
    def peso(self, val):
        if val <= 0:
            raise ValueError("Peso inválido")
        self._peso = val


# ============================
# OPERACION TRANSPORTE
# ============================
class OperacionTransporte:
    contador = 1

    def __init__(self, operador, vehiculo, carga, distancia):
        self.id_op = OperacionTransporte.contador
        OperacionTransporte.contador += 1

        self.operador = operador
        self.vehiculo = vehiculo
        self.carga = carga
        self.distancia = distancia
        self.finalizada = False

    def validar_peso(self):
        if self.carga.peso > self.vehiculo.capacidad_tn:
            raise ValueError("Peso excede la capacidad del vehículo")

    def finalizar(self):
        self.finalizada = True

    def generar_reporte(self):
        rendimiento = self.vehiculo.calcular_rendimiento(self.distancia, self.carga.peso)
        return {
            "operacion": self.id_op,
            "vehiculo": self.vehiculo.id_vehiculo,
            "peso": self.carga.peso,
            "rendimiento": rendimiento
        }


# ============================
# ALMACÉN (AGREGACIÓN)
# ============================
class AlmacenMineral:
    def __init__(self):
        self.inventario = {}

    def registrar_ingreso(self, operacion):
        if not operacion.finalizada:
            raise ValueError("Solo operaciones finalizadas pueden registrarse")
        tipo = operacion.carga.tipo
        peso = operacion.carga.peso
        if tipo not in self.inventario:
            self.inventario[tipo] = 0.0
        self.inventario[tipo] += peso

    def calcular_stock_total(self):
        return sum(self.inventario.values())


# ============================
# ESCENARIO (PRUEBA)
# ============================
def escenario():
    v1 = CamionTolva("T001", 20, 85)           # id, capacidad, resistencia
    v2 = VolqueteArticulado("V010", 35, 4)     # id, capacidad, num_ejes
    v3 = CamionLigero("L100", 5, "Hidráulica") # id, capacidad, suspension

    op1 = OperadorCamion("Juan", "123", "AII")
    op2 = SupervisorTransporte("María", "456", "SUP")
    op3 = ControladorAlmacen("Luis", "789", "CTRL")

    op1.asociar_vehiculo(v1)
    op1.asociar_vehiculo(v3)

    almacen = AlmacenMineral()

    # operación válida
    carga1 = CargaMineral("Cobre", 2.5, 15)
    oper1 = OperacionTransporte(op1, v1, carga1, 12)
    oper1.validar_peso()
    op1.registrar_operacion(oper1)
    oper1.finalizar()
    almacen.registrar_ingreso(oper1)

    # operación válida
    carga2 = CargaMineral("Plata", 1.0, 25)
    oper2 = OperacionTransporte(op2, v2, carga2, 40)
    oper2.validar_peso()
    op2.registrar_operacion(oper2)
    oper2.finalizar()
    almacen.registrar_ingreso(oper2)

    # operación inválida (peso excede)
    try:
        carga3 = CargaMineral("Oro", 0.8, 6)
        oper3 = OperacionTransporte(op1, v3, carga3, 8)
        oper3.validar_peso()
    except Exception as e:
        print("Error esperado en oper3:", e)

    print("\nInventario final:", almacen.inventario)
    print("Stock total:", almacen.calcular_stock_total())

if __name__ == "__main__":
    escenario()