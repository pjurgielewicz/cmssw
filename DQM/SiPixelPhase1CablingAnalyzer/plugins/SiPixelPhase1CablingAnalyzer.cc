#include "DQM/SiPixelPhase1CablingAnalyzer/interface/SiPixelPhase1CablingAnalyzer.h"

#include <iostream>
#include <fstream>
#include <map>

using namespace std;

SiPixelPhase1CablingAnalyzer::SiPixelPhase1CablingAnalyzer(const edm::ParameterSet& iConfig)

{
   //now do what ever initialization is needed
   // usesResource("TFileService");

}

SiPixelPhase1CablingAnalyzer::~SiPixelPhase1CablingAnalyzer()
{

}

void
SiPixelPhase1CablingAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  using namespace edm;

	ESHandle < TrackerGeometry > theTrackerGeometry;
	iSetup.get < TrackerDigiGeometryRecord > ().get(theTrackerGeometry);
  
  edm::ESHandle<SiPixelFedCablingMap> pixelFEDCablingMap;
  iSetup.get<SiPixelFedCablingMapRcd>().get(pixelFEDCablingMap);
	
	// edm::ESHandle<TrackerTopology> trackerTopologyHandle;
	// iSetup.get<TrackerTopologyRcd>().get(trackerTopologyHandle);
	
	// const TrackerTopology* tt = trackerTopologyHandle.operator->();
  
  auto pxb = theTrackerGeometry->detsPXB();
  
  auto cablingTree = pixelFEDCablingMap->cablingTree();
  
  // for (auto &i: pxb)
  // {
    // const GeomDet *det = i;
    // PXBDetId id = det->geographicalId();
    // unsigned rawid = id.rawId();
    
    // auto pixelFEDCab = cablingTree->fed(rawid);
    
    // // pixelFEDCab->print();
  // }
  
  std::vector<const SiPixelFedCablingTree::PixelFEDCabling*> fedCabling = cablingTree->fedList();
  // cout << "FED list size: " << fedCabling.size() << endl;
  
  std::map < unsigned, std::vector<unsigned> > dataDic;
  
  for (auto& fed: fedCabling) // through all feds
  {
    // cout << "FED id: " << fed->id() << endl;
    
    unsigned i = 1; 
    const sipixelobjects::PixelFEDLink* link = nullptr;
    while( (link = fed->link(i)) )
    {
      // cout << "\tLNK id: " << link->id() << endl;
      
      if ( link->numberOfROCs() )
      {
        unsigned rawId = link->roc(1)->rawId();
        // cout << "\t\tRAWID: " << rawId << endl;
        
        auto& dataRef = dataDic[rawId];
        
        if ( dataRef.size() == 0 )
        {
          dataRef.push_back( fed->id() );
        }
        dataRef.push_back( link->id() );
      }
      
      ++i;
    }
  }
  ofstream file("dbCablData.dat");
  for ( auto& elem: dataDic )
  {
    unsigned fed = elem.second[0];
    file << elem.first << " " << fed << " "; 
    for ( unsigned i = 1; i < elem.second.size(); ++i )
    {
      file << elem.second[i] << "/";
    }
    file << endl;
  }
  file.close();
  // cout << cablingTree->print(34) << endl;

  // # MIN FED NUMBER: phase0 = 0 (FEDNumbering::MINSiPixelFEDID), phase1 = 1200 (FEDNumbering::MINSiPixeluTCAFEDID)
}

void 
SiPixelPhase1CablingAnalyzer::beginJob()
{

}

void 
SiPixelPhase1CablingAnalyzer::endJob() 
{

}

void
SiPixelPhase1CablingAnalyzer::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(SiPixelPhase1CablingAnalyzer);
