'''_1161.py

PointsWithWorstResults
'''


from mastapy.gears.ltca.cylindrical import _820
from mastapy._internal import constructor
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_POINTS_WITH_WORST_RESULTS = python_net_import('SMT.MastaAPI.Gears.Cylindrical', 'PointsWithWorstResults')


__docformat__ = 'restructuredtext en'
__all__ = ('PointsWithWorstResults',)


class PointsWithWorstResults(_0.APIBase):
    '''PointsWithWorstResults

    This is a mastapy class.
    '''

    TYPE = _POINTS_WITH_WORST_RESULTS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PointsWithWorstResults.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def max_pressure(self) -> '_820.CylindricalGearMeshLoadedContactPoint':
        '''CylindricalGearMeshLoadedContactPoint: 'MaxPressure' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_820.CylindricalGearMeshLoadedContactPoint)(self.wrapped.MaxPressure) if self.wrapped.MaxPressure is not None else None

    @property
    def force_per_unit_length(self) -> '_820.CylindricalGearMeshLoadedContactPoint':
        '''CylindricalGearMeshLoadedContactPoint: 'ForcePerUnitLength' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_820.CylindricalGearMeshLoadedContactPoint)(self.wrapped.ForcePerUnitLength) if self.wrapped.ForcePerUnitLength is not None else None

    @property
    def hertzian_contact_half_width(self) -> '_820.CylindricalGearMeshLoadedContactPoint':
        '''CylindricalGearMeshLoadedContactPoint: 'HertzianContactHalfWidth' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_820.CylindricalGearMeshLoadedContactPoint)(self.wrapped.HertzianContactHalfWidth) if self.wrapped.HertzianContactHalfWidth is not None else None

    @property
    def max_shear_stress(self) -> '_820.CylindricalGearMeshLoadedContactPoint':
        '''CylindricalGearMeshLoadedContactPoint: 'MaxShearStress' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_820.CylindricalGearMeshLoadedContactPoint)(self.wrapped.MaxShearStress) if self.wrapped.MaxShearStress is not None else None

    @property
    def depth_of_max_shear_stress(self) -> '_820.CylindricalGearMeshLoadedContactPoint':
        '''CylindricalGearMeshLoadedContactPoint: 'DepthOfMaxShearStress' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_820.CylindricalGearMeshLoadedContactPoint)(self.wrapped.DepthOfMaxShearStress) if self.wrapped.DepthOfMaxShearStress is not None else None

    @property
    def total_deflection_for_mesh(self) -> '_820.CylindricalGearMeshLoadedContactPoint':
        '''CylindricalGearMeshLoadedContactPoint: 'TotalDeflectionForMesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_820.CylindricalGearMeshLoadedContactPoint)(self.wrapped.TotalDeflectionForMesh) if self.wrapped.TotalDeflectionForMesh is not None else None

    @property
    def sliding_velocity(self) -> '_820.CylindricalGearMeshLoadedContactPoint':
        '''CylindricalGearMeshLoadedContactPoint: 'SlidingVelocity' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_820.CylindricalGearMeshLoadedContactPoint)(self.wrapped.SlidingVelocity) if self.wrapped.SlidingVelocity is not None else None

    @property
    def pressure_velocity_pv(self) -> '_820.CylindricalGearMeshLoadedContactPoint':
        '''CylindricalGearMeshLoadedContactPoint: 'PressureVelocityPV' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_820.CylindricalGearMeshLoadedContactPoint)(self.wrapped.PressureVelocityPV) if self.wrapped.PressureVelocityPV is not None else None

    @property
    def minimum_lubricant_film_thickness_isotr1514412010(self) -> '_820.CylindricalGearMeshLoadedContactPoint':
        '''CylindricalGearMeshLoadedContactPoint: 'MinimumLubricantFilmThicknessISOTR1514412010' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_820.CylindricalGearMeshLoadedContactPoint)(self.wrapped.MinimumLubricantFilmThicknessISOTR1514412010) if self.wrapped.MinimumLubricantFilmThicknessISOTR1514412010 is not None else None

    @property
    def specific_lubricant_film_thickness_isotr1514412010(self) -> '_820.CylindricalGearMeshLoadedContactPoint':
        '''CylindricalGearMeshLoadedContactPoint: 'SpecificLubricantFilmThicknessISOTR1514412010' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_820.CylindricalGearMeshLoadedContactPoint)(self.wrapped.SpecificLubricantFilmThicknessISOTR1514412010) if self.wrapped.SpecificLubricantFilmThicknessISOTR1514412010 is not None else None

    @property
    def micropitting_safety_factor_isotr1514412010(self) -> '_820.CylindricalGearMeshLoadedContactPoint':
        '''CylindricalGearMeshLoadedContactPoint: 'MicropittingSafetyFactorISOTR1514412010' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_820.CylindricalGearMeshLoadedContactPoint)(self.wrapped.MicropittingSafetyFactorISOTR1514412010) if self.wrapped.MicropittingSafetyFactorISOTR1514412010 is not None else None

    @property
    def micropitting_flash_temperature_isotr1514412010(self) -> '_820.CylindricalGearMeshLoadedContactPoint':
        '''CylindricalGearMeshLoadedContactPoint: 'MicropittingFlashTemperatureISOTR1514412010' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_820.CylindricalGearMeshLoadedContactPoint)(self.wrapped.MicropittingFlashTemperatureISOTR1514412010) if self.wrapped.MicropittingFlashTemperatureISOTR1514412010 is not None else None

    @property
    def micropitting_contact_temperature_isotr1514412010(self) -> '_820.CylindricalGearMeshLoadedContactPoint':
        '''CylindricalGearMeshLoadedContactPoint: 'MicropittingContactTemperatureISOTR1514412010' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_820.CylindricalGearMeshLoadedContactPoint)(self.wrapped.MicropittingContactTemperatureISOTR1514412010) if self.wrapped.MicropittingContactTemperatureISOTR1514412010 is not None else None

    @property
    def minimum_lubricant_film_thickness_isotr1514412014(self) -> '_820.CylindricalGearMeshLoadedContactPoint':
        '''CylindricalGearMeshLoadedContactPoint: 'MinimumLubricantFilmThicknessISOTR1514412014' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_820.CylindricalGearMeshLoadedContactPoint)(self.wrapped.MinimumLubricantFilmThicknessISOTR1514412014) if self.wrapped.MinimumLubricantFilmThicknessISOTR1514412014 is not None else None

    @property
    def specific_lubricant_film_thickness_isotr1514412014(self) -> '_820.CylindricalGearMeshLoadedContactPoint':
        '''CylindricalGearMeshLoadedContactPoint: 'SpecificLubricantFilmThicknessISOTR1514412014' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_820.CylindricalGearMeshLoadedContactPoint)(self.wrapped.SpecificLubricantFilmThicknessISOTR1514412014) if self.wrapped.SpecificLubricantFilmThicknessISOTR1514412014 is not None else None

    @property
    def micropitting_safety_factor_isotr1514412014(self) -> '_820.CylindricalGearMeshLoadedContactPoint':
        '''CylindricalGearMeshLoadedContactPoint: 'MicropittingSafetyFactorISOTR1514412014' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_820.CylindricalGearMeshLoadedContactPoint)(self.wrapped.MicropittingSafetyFactorISOTR1514412014) if self.wrapped.MicropittingSafetyFactorISOTR1514412014 is not None else None

    @property
    def micropitting_flash_temperature_isotr1514412014(self) -> '_820.CylindricalGearMeshLoadedContactPoint':
        '''CylindricalGearMeshLoadedContactPoint: 'MicropittingFlashTemperatureISOTR1514412014' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_820.CylindricalGearMeshLoadedContactPoint)(self.wrapped.MicropittingFlashTemperatureISOTR1514412014) if self.wrapped.MicropittingFlashTemperatureISOTR1514412014 is not None else None

    @property
    def micropitting_contact_temperature_isotr1514412014(self) -> '_820.CylindricalGearMeshLoadedContactPoint':
        '''CylindricalGearMeshLoadedContactPoint: 'MicropittingContactTemperatureISOTR1514412014' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_820.CylindricalGearMeshLoadedContactPoint)(self.wrapped.MicropittingContactTemperatureISOTR1514412014) if self.wrapped.MicropittingContactTemperatureISOTR1514412014 is not None else None

    @property
    def minimum_lubricant_film_thickness_isots6336222018(self) -> '_820.CylindricalGearMeshLoadedContactPoint':
        '''CylindricalGearMeshLoadedContactPoint: 'MinimumLubricantFilmThicknessISOTS6336222018' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_820.CylindricalGearMeshLoadedContactPoint)(self.wrapped.MinimumLubricantFilmThicknessISOTS6336222018) if self.wrapped.MinimumLubricantFilmThicknessISOTS6336222018 is not None else None

    @property
    def specific_lubricant_film_thickness_isots6336222018(self) -> '_820.CylindricalGearMeshLoadedContactPoint':
        '''CylindricalGearMeshLoadedContactPoint: 'SpecificLubricantFilmThicknessISOTS6336222018' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_820.CylindricalGearMeshLoadedContactPoint)(self.wrapped.SpecificLubricantFilmThicknessISOTS6336222018) if self.wrapped.SpecificLubricantFilmThicknessISOTS6336222018 is not None else None

    @property
    def micropitting_safety_factor_isots6336222018(self) -> '_820.CylindricalGearMeshLoadedContactPoint':
        '''CylindricalGearMeshLoadedContactPoint: 'MicropittingSafetyFactorISOTS6336222018' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_820.CylindricalGearMeshLoadedContactPoint)(self.wrapped.MicropittingSafetyFactorISOTS6336222018) if self.wrapped.MicropittingSafetyFactorISOTS6336222018 is not None else None

    @property
    def micropitting_flash_temperature_isots6336222018(self) -> '_820.CylindricalGearMeshLoadedContactPoint':
        '''CylindricalGearMeshLoadedContactPoint: 'MicropittingFlashTemperatureISOTS6336222018' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_820.CylindricalGearMeshLoadedContactPoint)(self.wrapped.MicropittingFlashTemperatureISOTS6336222018) if self.wrapped.MicropittingFlashTemperatureISOTS6336222018 is not None else None

    @property
    def micropitting_contact_temperature_isots6336222018(self) -> '_820.CylindricalGearMeshLoadedContactPoint':
        '''CylindricalGearMeshLoadedContactPoint: 'MicropittingContactTemperatureISOTS6336222018' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_820.CylindricalGearMeshLoadedContactPoint)(self.wrapped.MicropittingContactTemperatureISOTS6336222018) if self.wrapped.MicropittingContactTemperatureISOTS6336222018 is not None else None

    @property
    def coefficient_of_friction_benedict_and_kelley(self) -> '_820.CylindricalGearMeshLoadedContactPoint':
        '''CylindricalGearMeshLoadedContactPoint: 'CoefficientOfFrictionBenedictAndKelley' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_820.CylindricalGearMeshLoadedContactPoint)(self.wrapped.CoefficientOfFrictionBenedictAndKelley) if self.wrapped.CoefficientOfFrictionBenedictAndKelley is not None else None

    @property
    def sliding_power_loss(self) -> '_820.CylindricalGearMeshLoadedContactPoint':
        '''CylindricalGearMeshLoadedContactPoint: 'SlidingPowerLoss' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_820.CylindricalGearMeshLoadedContactPoint)(self.wrapped.SlidingPowerLoss) if self.wrapped.SlidingPowerLoss is not None else None

    @property
    def scuffing_flash_temperature_isotr1398912000(self) -> '_820.CylindricalGearMeshLoadedContactPoint':
        '''CylindricalGearMeshLoadedContactPoint: 'ScuffingFlashTemperatureISOTR1398912000' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_820.CylindricalGearMeshLoadedContactPoint)(self.wrapped.ScuffingFlashTemperatureISOTR1398912000) if self.wrapped.ScuffingFlashTemperatureISOTR1398912000 is not None else None

    @property
    def scuffing_contact_temperature_isotr1398912000(self) -> '_820.CylindricalGearMeshLoadedContactPoint':
        '''CylindricalGearMeshLoadedContactPoint: 'ScuffingContactTemperatureISOTR1398912000' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_820.CylindricalGearMeshLoadedContactPoint)(self.wrapped.ScuffingContactTemperatureISOTR1398912000) if self.wrapped.ScuffingContactTemperatureISOTR1398912000 is not None else None

    @property
    def scuffing_safety_factor_isotr1398912000(self) -> '_820.CylindricalGearMeshLoadedContactPoint':
        '''CylindricalGearMeshLoadedContactPoint: 'ScuffingSafetyFactorISOTR1398912000' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_820.CylindricalGearMeshLoadedContactPoint)(self.wrapped.ScuffingSafetyFactorISOTR1398912000) if self.wrapped.ScuffingSafetyFactorISOTR1398912000 is not None else None

    @property
    def scuffing_flash_temperature_isots6336202017(self) -> '_820.CylindricalGearMeshLoadedContactPoint':
        '''CylindricalGearMeshLoadedContactPoint: 'ScuffingFlashTemperatureISOTS6336202017' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_820.CylindricalGearMeshLoadedContactPoint)(self.wrapped.ScuffingFlashTemperatureISOTS6336202017) if self.wrapped.ScuffingFlashTemperatureISOTS6336202017 is not None else None

    @property
    def scuffing_contact_temperature_isots6336202017(self) -> '_820.CylindricalGearMeshLoadedContactPoint':
        '''CylindricalGearMeshLoadedContactPoint: 'ScuffingContactTemperatureISOTS6336202017' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_820.CylindricalGearMeshLoadedContactPoint)(self.wrapped.ScuffingContactTemperatureISOTS6336202017) if self.wrapped.ScuffingContactTemperatureISOTS6336202017 is not None else None

    @property
    def scuffing_safety_factor_isots6336202017(self) -> '_820.CylindricalGearMeshLoadedContactPoint':
        '''CylindricalGearMeshLoadedContactPoint: 'ScuffingSafetyFactorISOTS6336202017' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_820.CylindricalGearMeshLoadedContactPoint)(self.wrapped.ScuffingSafetyFactorISOTS6336202017) if self.wrapped.ScuffingSafetyFactorISOTS6336202017 is not None else None

    @property
    def scuffing_flash_temperature_agma925a03(self) -> '_820.CylindricalGearMeshLoadedContactPoint':
        '''CylindricalGearMeshLoadedContactPoint: 'ScuffingFlashTemperatureAGMA925A03' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_820.CylindricalGearMeshLoadedContactPoint)(self.wrapped.ScuffingFlashTemperatureAGMA925A03) if self.wrapped.ScuffingFlashTemperatureAGMA925A03 is not None else None

    @property
    def scuffing_contact_temperature_agma925a03(self) -> '_820.CylindricalGearMeshLoadedContactPoint':
        '''CylindricalGearMeshLoadedContactPoint: 'ScuffingContactTemperatureAGMA925A03' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_820.CylindricalGearMeshLoadedContactPoint)(self.wrapped.ScuffingContactTemperatureAGMA925A03) if self.wrapped.ScuffingContactTemperatureAGMA925A03 is not None else None

    @property
    def scuffing_safety_factor_agma925a03(self) -> '_820.CylindricalGearMeshLoadedContactPoint':
        '''CylindricalGearMeshLoadedContactPoint: 'ScuffingSafetyFactorAGMA925A03' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_820.CylindricalGearMeshLoadedContactPoint)(self.wrapped.ScuffingSafetyFactorAGMA925A03) if self.wrapped.ScuffingSafetyFactorAGMA925A03 is not None else None

    @property
    def scuffing_flash_temperature_din399041987(self) -> '_820.CylindricalGearMeshLoadedContactPoint':
        '''CylindricalGearMeshLoadedContactPoint: 'ScuffingFlashTemperatureDIN399041987' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_820.CylindricalGearMeshLoadedContactPoint)(self.wrapped.ScuffingFlashTemperatureDIN399041987) if self.wrapped.ScuffingFlashTemperatureDIN399041987 is not None else None

    @property
    def scuffing_contact_temperature_din399041987(self) -> '_820.CylindricalGearMeshLoadedContactPoint':
        '''CylindricalGearMeshLoadedContactPoint: 'ScuffingContactTemperatureDIN399041987' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_820.CylindricalGearMeshLoadedContactPoint)(self.wrapped.ScuffingContactTemperatureDIN399041987) if self.wrapped.ScuffingContactTemperatureDIN399041987 is not None else None

    @property
    def scuffing_safety_factor_din399041987(self) -> '_820.CylindricalGearMeshLoadedContactPoint':
        '''CylindricalGearMeshLoadedContactPoint: 'ScuffingSafetyFactorDIN399041987' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_820.CylindricalGearMeshLoadedContactPoint)(self.wrapped.ScuffingSafetyFactorDIN399041987) if self.wrapped.ScuffingSafetyFactorDIN399041987 is not None else None

    @property
    def gap_between_loaded_flanks_transverse(self) -> '_820.CylindricalGearMeshLoadedContactPoint':
        '''CylindricalGearMeshLoadedContactPoint: 'GapBetweenLoadedFlanksTransverse' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_820.CylindricalGearMeshLoadedContactPoint)(self.wrapped.GapBetweenLoadedFlanksTransverse) if self.wrapped.GapBetweenLoadedFlanksTransverse is not None else None

    @property
    def gap_between_unloaded_flanks_transverse(self) -> '_820.CylindricalGearMeshLoadedContactPoint':
        '''CylindricalGearMeshLoadedContactPoint: 'GapBetweenUnloadedFlanksTransverse' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_820.CylindricalGearMeshLoadedContactPoint)(self.wrapped.GapBetweenUnloadedFlanksTransverse) if self.wrapped.GapBetweenUnloadedFlanksTransverse is not None else None

    @property
    def gear_a_maximum_material_exposure_iso633642019(self) -> '_820.CylindricalGearMeshLoadedContactPoint':
        '''CylindricalGearMeshLoadedContactPoint: 'GearAMaximumMaterialExposureISO633642019' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_820.CylindricalGearMeshLoadedContactPoint)(self.wrapped.GearAMaximumMaterialExposureISO633642019) if self.wrapped.GearAMaximumMaterialExposureISO633642019 is not None else None

    @property
    def gear_a_depth_of_maximum_material_exposure_iso633642019(self) -> '_820.CylindricalGearMeshLoadedContactPoint':
        '''CylindricalGearMeshLoadedContactPoint: 'GearADepthOfMaximumMaterialExposureISO633642019' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_820.CylindricalGearMeshLoadedContactPoint)(self.wrapped.GearADepthOfMaximumMaterialExposureISO633642019) if self.wrapped.GearADepthOfMaximumMaterialExposureISO633642019 is not None else None

    @property
    def gear_b_maximum_material_exposure_iso633642019(self) -> '_820.CylindricalGearMeshLoadedContactPoint':
        '''CylindricalGearMeshLoadedContactPoint: 'GearBMaximumMaterialExposureISO633642019' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_820.CylindricalGearMeshLoadedContactPoint)(self.wrapped.GearBMaximumMaterialExposureISO633642019) if self.wrapped.GearBMaximumMaterialExposureISO633642019 is not None else None

    @property
    def gear_b_depth_of_maximum_material_exposure_iso633642019(self) -> '_820.CylindricalGearMeshLoadedContactPoint':
        '''CylindricalGearMeshLoadedContactPoint: 'GearBDepthOfMaximumMaterialExposureISO633642019' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_820.CylindricalGearMeshLoadedContactPoint)(self.wrapped.GearBDepthOfMaximumMaterialExposureISO633642019) if self.wrapped.GearBDepthOfMaximumMaterialExposureISO633642019 is not None else None
