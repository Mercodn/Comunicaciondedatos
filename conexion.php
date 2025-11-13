<?php
require_once __DIR__ . '/vendor/autoload.php';

use Dotenv\Dotenv;

// Carga el .env desde la ruta del proyecto
$dotenv = Dotenv::createImmutable(__DIR__);
$dotenv->load();

// Mostrar variables cargadas (para depuración)
echo "<pre>";
print_r($_ENV);
echo "</pre>";

// Conexión MySQL usando las claves correctas
$conexion = new mysqli(
    $_ENV['DB_HOST'],
    $_ENV['DB_USER'],
    $_ENV['DB_PASSWORD'],
    $_ENV['DB_NAME']
);

if ($conexion->connect_error) {
    die("❌ Error de conexión: " . $conexion->connect_error);
}

echo "✅ Conectado correctamente a la base de datos '" . $_ENV['DB_NAME'] . "'";
?>
