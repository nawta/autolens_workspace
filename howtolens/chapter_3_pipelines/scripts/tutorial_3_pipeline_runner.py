# Up to now, we've not paid much attention to the source galaxy's morphology. We've assumed its a single-component
# exponential profile, which is a fairly crude assumption. A quick look at any image of a real galaxy reveals a wealth
# of different structures that could be present - bulges, disks, bars, star-forming knots and so on.
# Furthermore, there could be more than one source-galaxy!

# In this example, we'll explore how far we can get trying to_fit a complex source using a pipeline. Fitting complex
# source's is an exercise in diminishing returns. Each component we add to our source model brings with it an extra 5-7,
# parameters. If there are 4 components, or multiple galaxies, we're quickly entering the somewhat nasty regime of
# 30-40+ parameters in our non-linear search. Even with a pipeline, that is a lot of parameters to fit!

### AUTOFIT + CONFIG SETUP ###

import autofit as af

# Setup the path to the workspace, using by filling in your path below.
workspace_path = "/path/to/user/autolens_workspace/"
workspace_path = "/home/jammy/PycharmProjects/PyAutoLens/workspace/"

# Setup the path to the config folder, using the workspace path.
config_path = workspace_path + "config"

# Use this path to explicitly set the config path and output path.
af.conf.instance = af.conf.Config(
    config_path=config_path, output_path=workspace_path + "output"
)

### AUTOLENS + DATA SETUP ###

import autolens as al

# This function simulates an image with a complex source.
def simulate():

    psf = al.PSF.from_gaussian(shape=(11, 11), sigma=0.05, pixel_scale=0.05)

    grid = al.Grid.from_shape_pixel_scale_and_sub_grid_size(
        shape=(180, 180), pixel_scale=0.05
    )

    lens_galaxy = al.Galaxy(
        redshift=0.5,
        mass=al.mass_profiles.EllipticalIsothermal(
            centre=(0.0, 0.0), axis_ratio=0.8, phi=135.0, einstein_radius=1.6
        ),
    )

    source_galaxy_0 = al.Galaxy(
        redshift=1.0,
        light=al.light_profiles.EllipticalSersic(
            centre=(0.1, 0.1),
            axis_ratio=0.8,
            phi=90.0,
            intensity=0.2,
            effective_radius=1.0,
            sersic_index=1.5,
        ),
    )

    source_galaxy_1 = al.Galaxy(
        redshift=1.0,
        light=al.light_profiles.EllipticalSersic(
            centre=(-0.25, 0.25),
            axis_ratio=0.7,
            phi=45.0,
            intensity=0.1,
            effective_radius=0.2,
            sersic_index=3.0,
        ),
    )

    source_galaxy_2 = al.Galaxy(
        redshift=1.0,
        light=al.light_profiles.EllipticalSersic(
            centre=(0.45, -0.35),
            axis_ratio=0.6,
            phi=90.0,
            intensity=0.03,
            effective_radius=0.3,
            sersic_index=3.5,
        ),
    )

    source_galaxy_3 = al.Galaxy(
        redshift=1.0,
        light=al.light_profiles.EllipticalSersic(
            centre=(-0.05, -0.0),
            axis_ratio=0.9,
            phi=140.0,
            intensity=0.03,
            effective_radius=0.1,
            sersic_index=4.0,
        ),
    )

    tracer = al.Tracer.from_galaxies(
        galaxies=[
            lens_galaxy,
            source_galaxy_0,
            source_galaxy_1,
            source_galaxy_2,
            source_galaxy_3,
        ]
    )

    return al.SimulatedCCDData.from_tracer_grid_and_exposure_arrays(
        tracer=tracer,
        grid=grid,
        pixel_scale=0.05,
        exposure_time=300.0,
        psf=psf,
        background_sky_level=0.1,
        add_noise=True,
    )


# Lets Simulate the CCD data.
ccd_data = simulate()
al.ccd_plotters.plot_ccd_subplot(ccd_data=ccd_data)

# Yep, that's a pretty complex source. There are clearly more than 4 peaks of light - I wouldn't like to guess whether
# there is one or two sources (or more). You'll also notice I omitted the lens galaxy's light for this system. This is
# to keep the number of parameters down and the phases running fast, but we wouldn't get such a luxury for a real galaxy.

# Again, before we checkout the pipeline, lets import it, and get it running.
from autolens_workspace.howtolens.chapter_3_pipelines import tutorial_3_pipeline_complex_source

pipeline_complex_source = tutorial_3_pipeline_complex_source.make_pipeline(
    phase_folders=["howtolens", "c3_t3_complex_source"]
)

pipeline_complex_source.run(data=ccd_data)

# Okay, so with 4 sources, we still couldn't get a good a fit to the source that didn't leave residuals. However, I actually
# simulated the lens with 4 sources. This means that there is a 'perfect fit' somewhere in parameter
# space that we unfortunately missed using the pipeline above.

# Lets confirm this, by manually fitting the ccd data with the true input model.

lens_data = al.LensData(
    ccd_data=ccd_data,
    mask=al.Mask.circular(
        shape=ccd_data.shape, pixel_scale=ccd_data.pixel_scale, radius_arcsec=3.0
    ),
)

lens_galaxy = al.Galaxy(
    redshift=0.5,
    mass=al.mass_profiles.EllipticalIsothermal(
        centre=(0.0, 0.0), axis_ratio=0.8, phi=135.0, einstein_radius=1.6
    ),
)

source_galaxy_0 = al.Galaxy(
    redshift=1.0,
    light=al.light_profiles.EllipticalSersic(
        centre=(0.1, 0.1),
        axis_ratio=0.8,
        phi=90.0,
        intensity=0.2,
        effective_radius=1.0,
        sersic_index=1.5,
    ),
)

source_galaxy_1 = al.Galaxy(
    redshift=1.0,
    light=al.light_profiles.EllipticalSersic(
        centre=(-0.25, 0.25),
        axis_ratio=0.7,
        phi=45.0,
        intensity=0.1,
        effective_radius=0.2,
        sersic_index=3.0,
    ),
)

source_galaxy_2 = al.Galaxy(
    redshift=1.0,
    light=al.light_profiles.EllipticalSersic(
        centre=(0.45, -0.35),
        axis_ratio=0.6,
        phi=90.0,
        intensity=0.03,
        effective_radius=0.3,
        sersic_index=3.5,
    ),
)

source_galaxy_3 = al.Galaxy(
    redshift=1.0,
    light=al.light_profiles.EllipticalSersic(
        centre=(-0.05, -0.0),
        axis_ratio=0.9,
        phi=140.0,
        intensity=0.03,
        effective_radius=0.1,
        sersic_index=4.0,
    ),
)

tracer = al.Tracer.from_galaxies(
    galaxies=[
        lens_galaxy,
        source_galaxy_0,
        source_galaxy_1,
        source_galaxy_2,
        source_galaxy_3,
    ]
)

true_fit = al.LensDataFit.for_data_and_tracer(lens_data=lens_data, tracer=tracer)

al.lens_fit_plotters.plot_fit_subplot(
    fit=true_fit,
    should_plot_mask=True,
    extract_array_from_mask=True,
    zoom_around_mask=True,
)

al.lens_fit_plotters.plot_fit_subplot_of_planes(
    fit=true_fit,
    should_plot_mask=True,
    extract_array_from_mask=True,
    zoom_around_mask=True,
)

# And indeed, we see an improved residual-map, chi-squared-mao, and so forth.

# The morale of this story is that if the source morphology is complex, there is no way we can build a pipeline to
# fit it. For this tutorial, this was true even though our source model could actually fit the data perfectly. For
# real lenses, the source will be *even more complex* and there is even less hope of getting a good fit :(

# But fear not, PyAutoLens has you covered. In chapter 4, we'll introduce a completely new way to model the source
# galaxy, which addresses the problem faced here. But before that, in the next tutorial we'll discuss how we actually
# pass priors in a pipeline.
