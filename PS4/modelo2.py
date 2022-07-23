"""
Model exported as python.
Name : modelo2
Group : 
With QGIS : 32208
"""

# Imports
from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterRasterDestination
from qgis.core import QgsCoordinateReferenceSystem
import processing


# Modelo 2
class Modelo2(QgsProcessingAlgorithm):

    # Inicializacion del algoritmo
    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterRasterDestination('Suitout', 'suitout', createByDefault=True, defaultValue=None))

    # Definicion del algoritmo
    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model

        # Creacion del objeto feedback
        feedback = QgsProcessingMultiStepFeedback(2, model_feedback)

        # Creacion de diccionarios de resultados/outputs
        results = {}
        outputs = {}

        ######## Warp (reproject) ##########
        # Parametros de Warp (reproject)
        alg_params = {
            'DATA_TYPE': 0,  # Use Input Layer Data Type
            'EXTRA': '',
            'INPUT': 'suit_8c5c28bf_cf44_4d52_ba4b_ae44faa3834a',
            'MULTITHREADING': False,
            'NODATA': None,
            'OPTIONS': '',
            'RESAMPLING': 0,  # Nearest Neighbour
            'SOURCE_CRS': None,
            'TARGET_CRS': QgsCoordinateReferenceSystem('EPSG:4326'),  # CRS de destino
            'TARGET_EXTENT': None,
            'TARGET_EXTENT_CRS': None,
            'TARGET_RESOLUTION': None,
            'OUTPUT': parameters['Suitout']
        }

        # Corre warpreproject (de GDAL) con los parámetros de arriba y guarda el resultado
        # en el diccionario outputs (outputs = {'WarpReproject': ... })
        outputs['WarpReproject'] = processing.run('gdal:warpreproject', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        # Toma "OUTPUT" dentro de el 'WarpReproject' anterior y lo pasa a 
        # results (results = {'Suitout': ... })
        results['Suitout'] = outputs['WarpReproject']['OUTPUT']

        # Le cambia el paso al objeto feedback
        feedback.setCurrentStep(1)

        # Corta el proceso si feedback.isCanceled() == True
        if feedback.isCanceled():
            return {}

        ######## Extract projection ##########
        # Parametros de  Extract projection
        alg_params = {
            'INPUT': outputs['WarpReproject']['OUTPUT'],  # Output de warp reproject
            'PRJ_FILE_CREATE': True
        }

        # Corre extractprojection (de GDAL) con los parametros de arriba y guarda el resultado en
        # el diccionario outputs (outputs = {'WarpReproject': ... , 'ExtractProjection': '...'})
        outputs['ExtractProjection'] = processing.run('gdal:extractprojection', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        # Devuelve el diccionario results
        return results

    #### Definicion de parámetros generales del modelo ####
    
    # Nombre del modelo
    def name(self):
        return 'modelo2'

    # Nombre visible del modelo
    def displayName(self):
        return 'modelo2'

    # Grupo
    def group(self):
        return ''

    # ID del grupo
    def groupId(self):
        return ''

    # Función para crear instancia
    def createInstance(self):
        return Modelo2()
