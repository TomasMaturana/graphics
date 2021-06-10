use std::fs::File;

use rpt::*;

fn main() -> color_eyre::Result<()> {
    color_eyre::install()?;

    let mut scene = Scene::new();

    // Agregamos una casa
    scene.add(
        Object::new(
            load_obj(File::open("examples/table.obj")?)?
                .scale(&glm::vec3(2.0, 2.0, 2.0))
                .rotate_y(glm::pi())
                .translate(&glm::vec3(0.0, -1.0, -0.3)),
        )
        .material(Material::metallic(hex_color(0xf9e4b7), 0.4)),
    );

    // Agregamos un plano que simule un piso
    scene.add(
        Object::new(plane(glm::vec3(0.0, 1.0, 0.0), -1.0))
            .material(Material::diffuse(hex_color(0x918060))),
    );

    // Plano que simula cielo, para el eje Z
    scene.add(
        Object::new(plane(glm::vec3(0.0, 0.0, 1.0), -1.0)
            .translate(&glm::vec3(0.0, 0.0, -21.0))
        )
            .material(Material::diffuse(hex_color(0x87ceeb))),
    );

    // Plano de cielo para el eje X
    scene.add(
        Object::new(plane(glm::vec3(1.0, 0.0, 0.0), -1.0)
            .translate(&glm::vec3(21.0, 0.0, 0.0))
        )
            .material(Material::diffuse(hex_color(0x87ceeb))),
    );

    // Agregamos una luz ambiental
    scene.add(Light::Ambient(glm::vec3(0.5, 0.5, 0.5)));

    // Agregamos un punto de luz
    scene.add(Light::Point(
        glm::vec3(60.0, 60.0, 60.0),
        glm::vec3(0.0, 5.0, 0.0),
    ));

    let camera = Camera::look_at(
        glm::vec3(-2.5, 4.0, 6.5),
        glm::vec3(0.0, 0.0, 0.0),
        glm::vec3(0.0, 1.0, 0.0),
        std::f64::consts::FRAC_PI_6,
    );

    // Seteamos la camara y creamos la imagen, para cambiar la camara, podemos modificar el archivo camera, así es más sencillo :D
    Renderer::new(&scene, camera)
        .width(800)
        .height(800)
        .render()
        .save("mesa.png")?;

    Ok(())
}
