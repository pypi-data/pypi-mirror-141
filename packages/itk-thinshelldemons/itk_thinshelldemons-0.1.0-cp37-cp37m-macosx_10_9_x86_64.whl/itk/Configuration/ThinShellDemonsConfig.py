depends = ('ITKPyBase', 'ITKRegistrationMethodsv4', 'ITKRegistrationCommon', 'ITKQuadEdgeMeshFiltering', 'ITKQuadEdgeMesh', 'ITKOptimizersv4', 'ITKOptimizers', 'ITKMetricsv4', 'ITKMesh', 'ITKIOMeshBase', 'ITKCommon', )
templates = (  ('ThinShellDemonsMetricv4', 'itk::ThinShellDemonsMetricv4', 'itkThinShellDemonsMetricv4MF2', True, 'itk::Mesh< float,2 >'),
  ('ThinShellDemonsMetricv4', 'itk::ThinShellDemonsMetricv4', 'itkThinShellDemonsMetricv4MD2', True, 'itk::Mesh< double,2 >'),
  ('ThinShellDemonsMetricv4', 'itk::ThinShellDemonsMetricv4', 'itkThinShellDemonsMetricv4MF3', True, 'itk::Mesh< float,3 >'),
  ('ThinShellDemonsMetricv4', 'itk::ThinShellDemonsMetricv4', 'itkThinShellDemonsMetricv4MD3', True, 'itk::Mesh< double,3 >'),
  ('ThinShellDemonsMetricv4', 'itk::ThinShellDemonsMetricv4', 'itkThinShellDemonsMetricv4MF4', True, 'itk::Mesh< float,4 >'),
  ('ThinShellDemonsMetricv4', 'itk::ThinShellDemonsMetricv4', 'itkThinShellDemonsMetricv4MD4', True, 'itk::Mesh< double,4 >'),
  ('RegistrationParameterScalesFromPhysicalShift', 'itk::RegistrationParameterScalesFromPhysicalShift', 'itkRegistrationParameterScalesFromPhysicalShiftTSDMTMMMF2', False, 'itk::ThinShellDemonsMetricv4< itk::Mesh< float,2 > >'),
  ('RegistrationParameterScalesFromPhysicalShift', 'itk::RegistrationParameterScalesFromPhysicalShift', 'itkRegistrationParameterScalesFromPhysicalShiftTSDMTMMMD2', False, 'itk::ThinShellDemonsMetricv4< itk::Mesh< double,2 > >'),
  ('RegistrationParameterScalesFromPhysicalShift', 'itk::RegistrationParameterScalesFromPhysicalShift', 'itkRegistrationParameterScalesFromPhysicalShiftTSDMTMMMF3', False, 'itk::ThinShellDemonsMetricv4< itk::Mesh< float,3 > >'),
  ('RegistrationParameterScalesFromPhysicalShift', 'itk::RegistrationParameterScalesFromPhysicalShift', 'itkRegistrationParameterScalesFromPhysicalShiftTSDMTMMMD3', False, 'itk::ThinShellDemonsMetricv4< itk::Mesh< double,3 > >'),
  ('RegistrationParameterScalesFromPhysicalShift', 'itk::RegistrationParameterScalesFromPhysicalShift', 'itkRegistrationParameterScalesFromPhysicalShiftTSDMTMMMF4', False, 'itk::ThinShellDemonsMetricv4< itk::Mesh< float,4 > >'),
  ('RegistrationParameterScalesFromPhysicalShift', 'itk::RegistrationParameterScalesFromPhysicalShift', 'itkRegistrationParameterScalesFromPhysicalShiftTSDMTMMMD4', False, 'itk::ThinShellDemonsMetricv4< itk::Mesh< double,4 > >'),
)
