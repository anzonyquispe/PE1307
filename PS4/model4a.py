"""
Model exported as python.
Name : model4a
Group : 
With QGIS : 32208
"""
# importing all relevant libraries
from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterFeatureSink
import processing


# Generating class object for executing model
class Model4a(QgsProcessingAlgorithm):

    # Defining method to initialize the algorithm
    def initAlgorithm(self, config=None):
        # Defining A feature sink output for processing algorithms.
        # Importing raster
        self.addParameter(QgsProcessingParameterFeatureSink('Fixgeo_wlds', 
                    'fixgeo_wlds', 
                    type=QgsProcessing.TypeVectorAnyGeometry, 
                    createByDefault=True, 
                    supportsAppend=True, 
                    defaultValue=None))
        
        # Importing countries shapefiles
        self.addParameter(QgsProcessingParameterFeatureSink('Fixgeo_countries', 
                    'fixgeo_countries', 
                    type=QgsProcessing.TypeVectorAnyGeometry, 
                    createByDefault=True, 
                    supportsAppend=True, 
                    defaultValue=None))

        # Generting intersection output    
        self.addParameter(QgsProcessingParameterFeatureSink('Intersection', 
                    'intersection', 
                    type=QgsProcessing.TypeVectorAnyGeometry, 
                    createByDefault=True, 
                    defaultValue=None))

    # Method to process all algorithms
    def processAlgorithm(self, parameters, context, model_feedback):
        
        # Use a multi-step feedback, so that individual child 
        # algorithm progress reports are adjusted for the
        # overall progress through the model
        # Generating a contructor for every each step 
        # in QGIS model
        feedback = QgsProcessingMultiStepFeedback(4, model_feedback)
        # Generating dictionary for results
        results = {}
        # Generating dictionary for Outputs
        outputs = {}

        # Fix geometries ctry
        
        alg_params = {
            # Adding absolute path for countries shapfile.
            'INPUT': 'C:/Users/Anzony/Documents/GitHub/PE1307/_data/ne_10m_admin_0_countries/ne_10m_admin_0_countries.shp',
            # Naming the output
            'OUTPUT': parameters['Fixgeo_countries']
        }

        # Saving an object named as "FixGeometriesCtry" 
        # in the ouputs dictionary
        # Process for importing country shapefiles
        outputs['FixGeometriesCtry'] = processing.run('native:fixgeometries', 
                                            alg_params, 
                                            context=context, 
                                            feedback=feedback, 
                                            is_child_algorithm=True)

        # Saving the output of the processing result in "results" dictionary
        results['Fixgeo_countries'] = outputs['FixGeometriesCtry']['OUTPUT']


        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Fix geometries - lang
        alg_params = {
            # Path for "clean" file
            'INPUT': 'C:/Users/Anzony/Documents/GitHub/PE1307/_data/models/output/clean.gpkg',
            # Naming the shapefile as 'Fixgeo_wlds'
            'OUTPUT': parameters['Fixgeo_wlds']
        }

        # Processing the "Clean" file
        outputs['FixGeometriesLang'] = processing.run('native:fixgeometries', 
                    alg_params, context=context, 
                    feedback=feedback, is_child_algorithm=True)

        # Saving the return from the processing in the results dictionary
        results['Fixgeo_wlds'] = outputs['FixGeometriesLang']['OUTPUT']

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # Intersection
        # Generating the dictionary needed for intersection
        alg_params = {
            # Country Shapefiles
            'INPUT': outputs['FixGeometriesLang']['OUTPUT'],
            'INPUT_FIELDS': ['GID'],

            # Clean file
            'OVERLAY': outputs['FixGeometriesLang']['OUTPUT'],
            'OVERLAY_FIELDS': ['ADMIN'],
            'OVERLAY_FIELDS_PREFIX': '',

            # Naming for intersection
            'OUTPUT': parameters['Intersection']
        }

        # Intersecting Both shapefiles
        outputs['Intersection'] = processing.run('native:intersection', 
                alg_params, context=context, 
                feedback=feedback, is_child_algorithm=True)

        # Saving in the results dictionary
        results['Intersection'] = outputs['Intersection']['OUTPUT']

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # Statistics by categories
        # Generating the CSV file "languages_by_country"
        alg_params = {
            'CATEGORIES_FIELD_NAME': ['ADMIN'],
            'INPUT': outputs['FixGeometriesLang']['OUTPUT'],
            'OUTPUT': 'C:/Users/Anzony/Documents/GitHub/PE1307/_data/models/output/languages_by_country.csv',
            'VALUES_FIELD_NAME': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }

        # Generating the CSV file
        outputs['StatisticsByCategories'] = processing.run('qgis:statisticsbycategories', 
                alg_params, context=context, 
                feedback=feedback, is_child_algorithm=True)
        return results

    def name(self):
        return 'model4a'

    def displayName(self):
        return 'model4a'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return Model4a()
