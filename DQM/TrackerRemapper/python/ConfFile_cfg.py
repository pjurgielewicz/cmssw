import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing
from Configuration.AlCa.GlobalTag import GlobalTag

options = VarParsing.VarParsing("analysis")

MODE_ANALYZE, MODE_REMAP = 0, 1
RECHITS, DIGIS, CLUSTERS = 1, 2, 3

dataSourceDic = { RECHITS : "generalTracks",
                  DIGIS   : "siStripDigis",
                  CLUSTERS: "siStripClusters" }

defaultAnylyzeMode = RECHITS

###################### OPTIONS HANDLER

options.register ("opMode",                                  
                  MODE_REMAP,               
                  VarParsing.VarParsing.multiplicity.singleton, 
                  VarParsing.VarParsing.varType.int,         
                  "Operation Mode")   

options.register ("analyzeMode",                                  
                  defaultAnylyzeMode,               
                  VarParsing.VarParsing.multiplicity.singleton, 
                  VarParsing.VarParsing.varType.int,         
                  "Analyze Mode") 

options.register ("eventLimit",                                  
                  100,               
                  VarParsing.VarParsing.multiplicity.singleton, 
                  VarParsing.VarParsing.varType.int,         
                  "Limits Events Processed in Analyze Mode") 

options.register ("inputRootFile",                                  
                  "DQM_V0001_SiStrip_R000305516.root", 
                #   "file:RECO_file.root",   
                    # "/store/express/Run2017H/ExpressPhysics/FEVT/Express-v1/000/306/936/00000/ECE8DA52-3ACF-E711-84A0-02163E0141ED.root",                       
                  VarParsing.VarParsing.multiplicity.singleton, 
                  VarParsing.VarParsing.varType.string,         
                  "Source Data File - either for analyze or remap")   

options.register ("stripHistogram",                                  
                  "TkHMap_NumberValidHits",               
                  VarParsing.VarParsing.multiplicity.singleton, 
                  VarParsing.VarParsing.varType.string,         
                  "Strip Detector Histogram to Remap")   

options.register (
                  "src",   
                  dataSourceDic[defaultAnylyzeMode],                                              
                  VarParsing.VarParsing.multiplicity.singleton, 
                  VarParsing.VarParsing.varType.string,         
                  "Collection Source")    #??

options.register ("globalTag",                                  # option name
                  "90X_upgrade2017_realistic_v6",                # default value
                  VarParsing.VarParsing.multiplicity.singleton, # singleton or list
                  VarParsing.VarParsing.varType.string,         # string, bool, int, or float
                  "Global Tag")                                 # ? help ?
                  
options.parseArguments()

######################

process = cms.Process("Demo")

if options.opMode == MODE_ANALYZE:
    process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(options.eventLimit) )
    process.source = cms.Source("PoolSource",
        fileNames = cms.untracked.vstring(
            options.inputRootFile
        )
    )
    runNumber = "Analyze"

elif options.opMode == MODE_REMAP:
    process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1) )
    process.source = cms.Source("EmptySource")
    #run number deduction
    runNumber = str(int(options.inputRootFile.split("_")[-1].split(".")[0][1:]))

process.demo = cms.EDAnalyzer('TrackerRemapper',
                                opMode = cms.untracked.uint32(options.opMode),
                                analyzeMode = cms.untracked.uint32(options.analyzeMode),
                                stripRemapFile = cms.untracked.string(options.inputRootFile),
                                stripHistogram = cms.untracked.string(options.stripHistogram),
                                runString = cms.untracked.string(runNumber),
                                src = cms.InputTag(options.src),
                                )

process.p = cms.Path(process.demo)

process.load("Configuration.StandardSequences.GeometryRecoDB_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag = GlobalTag(process.GlobalTag, options.globalTag, "")

process.SiStripDetInfoFileReader = cms.Service("SiStripDetInfoFileReader")
process.TkDetMap = cms.Service("TkDetMap")

# Output root file name:
process.TFileService = cms.Service("TFileService", fileName = cms.string('outputStrip.root') )

