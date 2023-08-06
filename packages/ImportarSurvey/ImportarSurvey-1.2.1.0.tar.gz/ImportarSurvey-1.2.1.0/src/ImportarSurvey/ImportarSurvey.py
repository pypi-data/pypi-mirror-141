import os

from fileinput import filename
from ImportarSurvey.Utiles import JsonFile, ToolboxLogger
from ImportarSurvey.PrecargarEncuestas import PrecargarEncuestas
from ImportarSurvey.InyectarEncuestas import InyectarEncuestas
from ImportarSurvey.ArcGISPythonApiDataAccess import ArcGISPythonApiDataAccess

STATISTICS_FILE = "__estadisticas.json"
LOG_PATH = "../.."

class ProcesarEncuestas :

    @staticmethod 
    def BorrarEncuestas(
        portal = None, 
        usuario = None, 
        clave = None, 
        servicioEncuesta = None, 
        debug = False,
        rutaSalida = '', 
        salidaRelativa = False) :

        LOG_FILE = "__logBorrarEncuestasVSCode"
        alias = "LogBorrarEncuestasVSCode"

        folder_path = os.path.dirname(os.path.realpath(__file__))
        log_path = os.path.normpath(os.path.join(folder_path, LOG_PATH, rutaSalida)) if salidaRelativa else rutaSalida

        ToolboxLogger.initLogger(source=alias, log_path=log_path, log_file=LOG_FILE)
        ToolboxLogger.setDebugLevel() if debug else ToolboxLogger.setInfoLevel()

        ToolboxLogger.info("Iniciando {}".format(alias))
        ToolboxLogger.info("Ruta Salida: {}".format(log_path))
        fuente_da = ArcGISPythonApiDataAccess(portal, usuario, clave)
        fuente_da.setFeatureService(servicioEncuesta)

        numRegistros = 0

        for tabla in fuente_da.getServiceTables() :
            registros = fuente_da.query(tabla, [tabla.properties.objectIdField])
            fuente_da.delete(tabla, registros)
            numRegistros += len(registros)
            ToolboxLogger.debug("Tabla: {} Borrados: {}".format(tabla.properties.name, len(registros)))

        for capa in fuente_da.getServiceLayers() :
            registros = fuente_da.query(capa, [capa.properties.objectIdField])
            fuente_da.delete(capa, registros)
            numRegistros += len(registros)
            ToolboxLogger.debug("Capa: {} Borrados: {}".format(capa.properties.name, len(registros)))

        ToolboxLogger.info("Total Borrados: {}".format(numRegistros))

    @staticmethod
    def Precargar(portal = None, 
        usuario = None, 
        clave = None, 
        usuarioCampo = None,
        servicioFuente = None, 
        versionFuente = None, 
        servicioDestino = None, 
        idsPrecarga = None, 
        debug = False, 
        rutaSalida = '', 
        salidaRelativa = False) :

        LOG_BACKWARD_FILE = "__logPrecargarEncuestasVsCode"
        CONFIG_BACKWARD_PATH = "_precarga_geo.json"
        alias = "PrecargarEncuestasVSCode"

        folder_path = os.path.dirname(os.path.realpath(__file__))
        config_path = os.path.join(folder_path, CONFIG_BACKWARD_PATH)
        log_path = os.path.normpath(os.path.join(folder_path, LOG_PATH, rutaSalida)) if salidaRelativa else rutaSalida

        ToolboxLogger.initLogger(source = alias, log_path = log_path, log_file = LOG_BACKWARD_FILE)
        ToolboxLogger.setDebugLevel() if debug else ToolboxLogger.setInfoLevel()

        if servicioFuente and versionFuente and servicioDestino and idsPrecarga:
            ToolboxLogger.info("Iniciando {}".format(alias))
            ToolboxLogger.info("Ruta Salida: {}".format(log_path))

            encuestas = 0
            registros = 0
            errores = 0

            preloader = PrecargarEncuestas(config_path, 
                portal, 
                usuario, 
                clave,
                servicioFuente, 
                servicioDestino, 
                usuarioCampo= usuarioCampo,
                versionFuente = versionFuente,
                idsPrecarga = idsPrecarga
            )

            resultado  = preloader.Ejecutar()
            if resultado: 
                encuestas = resultado[0]
                registros = resultado[1]
                errores = resultado[2]
                version = preloader.versionFuente

            ToolboxLogger.info("Versión: {}".format(version))
            ToolboxLogger.info("Encuestas: {}".format(encuestas))
            ToolboxLogger.info("Registros: {}".format(registros))
            ToolboxLogger.info("Errores: {}".format(errores))

            filename = os.path.join(log_path, STATISTICS_FILE)
            registros = JsonFile.readFile(filename)

            registros.append(preloader.registroEjecucion())
            JsonFile.writeFile(filename, registros)
        else:
            if not servicioFuente:
                ToolboxLogger.info("No se definió Servicio Fuente")
            if not versionFuente:
                ToolboxLogger.info("No se definió Versión Fuente")
            if not servicioDestino:
                ToolboxLogger.info("No se definió Servicio Destino")
            if not idsPrecarga:
                ToolboxLogger.info("No se definieron IDs de Precarga")

    @staticmethod
    def Inyectar(portal = None, 
        usuario = None, 
        clave = None, 
        usuarioCampo = None,
        servicioFuente = None, 
        servicioDestino = None,
        versionDestino = None, 
        debug = False, 
        rutaSalida = '', 
        salidaRelativa = False) :

        LOG_FILE = "__logInyectarEncuestasVSCode"
        CONFIG_PATH = "_inyeccion_geo.json"

        alias = "LogInyectarEncuestasVSCode"

        folder_path = os.path.dirname(os.path.realpath(__file__))
        config_path = os.path.join(folder_path, CONFIG_PATH)
        log_path = os.path.normpath(os.path.join(folder_path, LOG_PATH, rutaSalida)) if salidaRelativa else rutaSalida

        ToolboxLogger.initLogger(source = alias, log_path = log_path, log_file = LOG_FILE)
        ToolboxLogger.setDebugLevel() if debug else ToolboxLogger.setInfoLevel()

        if servicioFuente and versionDestino and servicioDestino:
            ToolboxLogger.info("Iniciando {}".format(alias))
            ToolboxLogger.info("Ruta Salida: {}".format(log_path))

            encuestas = 0
            registros = 0
            errores = 0

            inyector = InyectarEncuestas(
                config_path, 
                portal, 
                usuario, 
                clave, 
                servicioFuente, 
                servicioDestino, 
                usuarioCampo = usuarioCampo,
                versionDestino = versionDestino
            )
            resultado  = inyector.Ejecutar()
            if resultado: 
                encuestas = resultado[0]
                registros = resultado[1]
                errores = resultado[2]
                versionFinal = inyector.versionDestino
            
            ToolboxLogger.info("Version Final: {}".format(versionFinal))
            ToolboxLogger.info("Encuestas: {}".format(encuestas))
            ToolboxLogger.info("Registros: {}".format(registros))
            ToolboxLogger.info("Errores: {}".format(errores))

            filename = os.path.join(log_path, STATISTICS_FILE)
            registros = JsonFile.readFile(filename)

            registros.append(inyector.registroEjecucion())
            JsonFile.writeFile(filename, registros)
        else:
            if not servicioFuente:
                ToolboxLogger.info("No se definió Servicio Fuente")
            if not servicioDestino:
                ToolboxLogger.info("No se definió Servicio Destino")
            if not versionDestino:
                ToolboxLogger.info("No se definió Versión Destino")

