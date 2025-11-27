
SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

CREATE TABLE `auth_group` (
  `id` int NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE `auth_permission` (
  `id` int NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add user', 4, 'add_user'),
(14, 'Can change user', 4, 'change_user'),
(15, 'Can delete user', 4, 'delete_user'),
(16, 'Can view user', 4, 'view_user'),
(17, 'Can add content type', 5, 'add_contenttype'),
(18, 'Can change content type', 5, 'change_contenttype'),
(19, 'Can delete content type', 5, 'delete_contenttype'),
(20, 'Can view content type', 5, 'view_contenttype'),
(21, 'Can add session', 6, 'add_session'),
(22, 'Can change session', 6, 'change_session'),
(23, 'Can delete session', 6, 'delete_session'),
(24, 'Can view session', 6, 'view_session'),
(25, 'Can add catalogo publico', 7, 'add_catalogopublico'),
(26, 'Can change catalogo publico', 7, 'change_catalogopublico'),
(27, 'Can delete catalogo publico', 7, 'delete_catalogopublico'),
(28, 'Can view catalogo publico', 7, 'view_catalogopublico'),
(29, 'Can add clientes', 8, 'add_clientes'),
(30, 'Can change clientes', 8, 'change_clientes'),
(31, 'Can delete clientes', 8, 'delete_clientes'),
(32, 'Can view clientes', 8, 'view_clientes'),
(33, 'Can add libros', 9, 'add_libros'),
(34, 'Can change libros', 9, 'change_libros'),
(35, 'Can delete libros', 9, 'delete_libros'),
(36, 'Can view libros', 9, 'view_libros'),
(37, 'Can add permisos', 10, 'add_permisos'),
(38, 'Can change permisos', 10, 'change_permisos'),
(39, 'Can delete permisos', 10, 'delete_permisos'),
(40, 'Can view permisos', 10, 'view_permisos'),
(41, 'Can add reglas prestamo', 11, 'add_reglasprestamo'),
(42, 'Can change reglas prestamo', 11, 'change_reglasprestamo'),
(43, 'Can delete reglas prestamo', 11, 'delete_reglasprestamo'),
(44, 'Can view reglas prestamo', 11, 'view_reglasprestamo'),
(45, 'Can add roles', 12, 'add_roles'),
(46, 'Can change roles', 12, 'change_roles'),
(47, 'Can delete roles', 12, 'delete_roles'),
(48, 'Can view roles', 12, 'view_roles'),
(49, 'Can add ejemplares', 13, 'add_ejemplares'),
(50, 'Can change ejemplares', 13, 'change_ejemplares'),
(51, 'Can delete ejemplares', 13, 'delete_ejemplares'),
(52, 'Can view ejemplares', 13, 'view_ejemplares'),
(53, 'Can add prestamos', 14, 'add_prestamos'),
(54, 'Can change prestamos', 14, 'change_prestamos'),
(55, 'Can delete prestamos', 14, 'delete_prestamos'),
(56, 'Can view prestamos', 14, 'view_prestamos'),
(57, 'Can add reservas', 15, 'add_reservas'),
(58, 'Can change reservas', 15, 'change_reservas'),
(59, 'Can delete reservas', 15, 'delete_reservas'),
(60, 'Can view reservas', 15, 'view_reservas'),
(61, 'Can add rol permiso', 16, 'add_rolpermiso'),
(62, 'Can change rol permiso', 16, 'change_rolpermiso'),
(63, 'Can delete rol permiso', 16, 'delete_rolpermiso'),
(64, 'Can view rol permiso', 16, 'view_rolpermiso'),
(65, 'Can add usuarios', 17, 'add_usuarios'),
(66, 'Can change usuarios', 17, 'change_usuarios'),
(67, 'Can delete usuarios', 17, 'delete_usuarios'),
(68, 'Can view usuarios', 17, 'view_usuarios'),
(69, 'Can add bitacora', 18, 'add_bitacora'),
(70, 'Can change bitacora', 18, 'change_bitacora'),
(71, 'Can delete bitacora', 18, 'delete_bitacora'),
(72, 'Can view bitacora', 18, 'view_bitacora'),
(73, 'Can add solicitud venta', 19, 'add_solicitudventa'),
(74, 'Can change solicitud venta', 19, 'change_solicitudventa'),
(75, 'Can delete solicitud venta', 19, 'delete_solicitudventa'),
(76, 'Can view solicitud venta', 19, 'view_solicitudventa'),
(77, 'Can add ventas', 20, 'add_ventas'),
(78, 'Can change ventas', 20, 'change_ventas'),
(79, 'Can delete ventas', 20, 'delete_ventas'),
(80, 'Can view ventas', 20, 'view_ventas'),
(81, 'Can add detalle venta', 21, 'add_detalleventa'),
(82, 'Can change detalle venta', 21, 'change_detalleventa'),
(83, 'Can delete detalle venta', 21, 'delete_detalleventa'),
(84, 'Can view detalle venta', 21, 'view_detalleventa'),
(85, 'Can add proveedores', 22, 'add_proveedores'),
(86, 'Can change proveedores', 22, 'change_proveedores'),
(87, 'Can delete proveedores', 22, 'delete_proveedores'),
(88, 'Can view proveedores', 22, 'view_proveedores'),
(89, 'Can add compras', 23, 'add_compras'),
(90, 'Can change compras', 23, 'change_compras'),
(91, 'Can delete compras', 23, 'delete_compras'),
(92, 'Can view compras', 23, 'view_compras'),
(93, 'Can add detalle compras', 24, 'add_detallecompras'),
(94, 'Can change detalle compras', 24, 'change_detallecompras'),
(95, 'Can delete detalle compras', 24, 'delete_detallecompras'),
(96, 'Can view detalle compras', 24, 'view_detallecompras');

CREATE TABLE `auth_user` (
  `id` int NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `auth_user_groups` (
  `id` bigint NOT NULL,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `auth_user_user_permissions` (
  `id` bigint NOT NULL,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `bitacora` (
  `id` bigint NOT NULL,
  `accion` varchar(255) NOT NULL,
  `fecha` datetime(6) DEFAULT NULL,
  `usuario_id` bigint DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `bitacora` (`id`, `accion`, `fecha`, `usuario_id`) VALUES
(1, 'REGISTRO EMPLEADO: juana@biblionet.com como bibliotecario', '2025-11-25 19:11:37.478141', 2),
(2, 'ACTUALIZÓ REGLAS DE PRÉSTAMO: plazo=10 días, límite=1, mora=25', '2025-11-25 19:19:48.216324', 2),
(3, 'REGISTRO PRÉSTAMO: cliente=0801200117457, ejemplar=EJ-1-6407, id_prestamo=1', '2025-11-25 19:22:58.598465', 3),
(4, 'BLOQUEÓ CLIENTE ID=1', '2025-11-25 19:45:55.998552', 2),
(5, 'DESBLOQUEÓ CLIENTE ID=1', '2025-11-25 19:46:47.565268', 2),
(6, 'DEVOLVIÓ PRÉSTAMO id=1 sin mora', '2025-11-25 20:08:03.658278', 3),
(7, 'REGISTRO PRÉSTAMO: cliente=0801200117457, ejemplar=EJ-1-5767, id_prestamo=2', '2025-11-25 20:08:17.446549', 3),
(8, 'RENOVÓ PRÉSTAMO id=2 nueva_fecha=2025-12-31', '2025-11-25 21:17:07.065263', 3),
(9, 'DEVOLVIÓ PRÉSTAMO id=2 sin mora', '2025-11-26 00:35:20.545370', 3),
(10, 'REGISTRO PRÉSTAMO: cliente=0801200117457, ejemplar=EJ-3-1195, id_prestamo=3', '2025-11-26 00:35:34.582833', 3),
(11, 'EDITO EL LIBRO: \'El señor de los anillos: La comunidad del anillo\'', '2025-11-26 17:03:02.562897', 3),
(12, 'DEVOLVIÓ PRÉSTAMO id=3 sin mora', '2025-11-26 17:13:51.609966', 3),
(13, 'REGISTRO PRÉSTAMO: cliente=0801200117457, ejemplar=EJ-3-3847, id_prestamo=4', '2025-11-26 17:14:04.816210', 3),
(14, 'ACTUALIZÓ REGLAS DE PRÉSTAMO: plazo=1 días, límite=2, mora=25.0', '2025-11-26 17:48:29.335903', 2),
(15, 'REGISTRO PRÉSTAMO: cliente=0801200117457, ejemplar=EJ-5-1853, id_prestamo=5', '2025-11-26 17:49:43.162692', 3),
(16, 'REGISTRÓ COMPRA id=1 factura=FAC-000001 proveedor=Distribuidora Librera Centroamericana S.A. de C.V. total=2000.0', '2025-11-26 21:42:47.049890', 2),
(17, 'REGISTRO EMPLEADO: maria@hotmail.com como bibliotecario', '2025-11-27 02:57:58.124416', 2),
(18, 'REGISTRÓ COMPRA id=2 factura=FAC-000002 proveedor=Libros Juan y Maria SA de CV total=3000.0', '2025-11-27 03:03:14.933026', 2),
(19, 'BLOQUEÓ CLIENTE ID=1', '2025-11-27 03:04:06.553427', 2),
(20, 'DESBLOQUEÓ CLIENTE ID=1', '2025-11-27 03:04:22.481076', 2),
(21, 'ACTUALIZÓ REGLAS DE PRÉSTAMO: plazo=1 días, límite=2, mora=30.0', '2025-11-27 03:05:04.571588', 2),
(22, 'ACTUALIZÓ REGLAS DE PRÉSTAMO: plazo=15 días, límite=2, mora=40.0', '2025-11-27 03:05:17.901967', 2),
(23, 'DEVOLVIÓ PRÉSTAMO id=4 sin mora', '2025-11-27 03:11:36.118362', 6),
(24, 'REGISTRO PRÉSTAMO: cliente=080120011456, ejemplar=EJ-7-4476, id_prestamo=6', '2025-11-27 03:12:24.154662', 6),
(25, 'RENOVÓ PRÉSTAMO id=6 nueva_fecha=2025-12-25', '2025-11-27 03:13:21.857252', 6),
(26, 'DEVOLVIÓ PRÉSTAMO id=6 sin mora', '2025-11-27 03:18:48.888599', 6),
(27, 'REGISTRO EMPLEADO: jose@biblionet.com como bibliotecario', '2025-11-27 04:18:39.169410', 2),
(28, 'REGISTRÓ COMPRA id=3 factura=FAC-000003 proveedor=Distribuidora Librera Centroamericana S.A. de C.V. total=3500.0', '2025-11-27 04:21:24.602990', 2),
(29, 'BLOQUEÓ CLIENTE ID=3', '2025-11-27 04:22:59.319278', 2),
(30, 'DESBLOQUEÓ CLIENTE ID=3', '2025-11-27 04:25:19.172751', 2),
(31, 'BLOQUEÓ CLIENTE ID=1', '2025-11-27 04:25:21.901273', 2),
(32, 'REGISTRO PRÉSTAMO: cliente=0801200117458, ejemplar=EJ-7-7646, id_prestamo=7', '2025-11-27 04:50:40.841016', 6),
(33, 'REGISTRO PRÉSTAMO: cliente=0801200117458, ejemplar=EJ-2-7662, id_prestamo=8', '2025-11-27 04:51:09.265670', 6),
(34, 'BLOQUEÓ CLIENTE ID=3', '2025-11-27 04:53:58.450237', 2),
(35, 'DESBLOQUEÓ CLIENTE ID=3', '2025-11-27 04:54:59.705231', 2),
(36, 'ACTUALIZÓ REGLAS DE PRÉSTAMO: plazo=10 días, límite=3, mora=50.0', '2025-11-27 04:55:30.713969', 2),
(37, 'BLOQUEÓ CLIENTE ID=3', '2025-11-27 04:58:34.447923', 2),
(38, 'DESBLOQUEÓ CLIENTE ID=3', '2025-11-27 04:59:30.729650', 2),
(39, 'ACTUALIZÓ REGLAS DE PRÉSTAMO: plazo=15 días, límite=2, mora=60.0', '2025-11-27 04:59:53.299072', 2),
(40, 'DEVOLVIÓ PRÉSTAMO id=8 sin mora', '2025-11-27 05:04:21.601283', 8),
(41, 'REGISTRO PRÉSTAMO: cliente=0801200117458, ejemplar=EJ-3-3352, id_prestamo=9', '2025-11-27 05:04:47.838353', 8),
(42, 'RENOVÓ PRÉSTAMO id=9 nueva_fecha=2025-12-20', '2025-11-27 05:05:30.343484', 8);

CREATE TABLE `clientes` (
  `id` bigint NOT NULL,
  `dni` varchar(20) NOT NULL,
  `direccion` varchar(255) DEFAULT NULL,
  `estado` varchar(20) NOT NULL,
  `bloqueado` tinyint(1) NOT NULL,
  `motivo_bloqueo` varchar(255) DEFAULT NULL,
  `fecha_bloqueo` datetime(6) DEFAULT NULL,
  `usuario_id` bigint NOT NULL,
  `telefono` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `clientes` (`id`, `dni`, `direccion`, `estado`, `bloqueado`, `motivo_bloqueo`, `fecha_bloqueo`, `usuario_id`, `telefono`) VALUES
(1, '0801200117457', 'Col. Miramesi', 'inactivo', 1, 'Bloqueado manualmente por el administrador.', '2025-11-27 04:25:21.891600', 1, NULL),
(2, '080120011456', 'Col Miramesi', 'activo', 0, NULL, NULL, 5, NULL),
(3, '0801200117458', 'Residencial Plaza', 'activo', 0, 'Bloqueado manualmente por el administrador.', '2025-11-27 04:58:34.438294', 7, NULL);

CREATE TABLE `compras` (
  `id` int NOT NULL,
  `numero_factura` varchar(50) NOT NULL,
  `fecha` datetime(6) DEFAULT NULL,
  `total` decimal(10,2) NOT NULL,
  `metodo_pago` varchar(50) DEFAULT NULL,
  `usuario_id` bigint NOT NULL,
  `proveedor_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `compras` (`id`, `numero_factura`, `fecha`, `total`, `metodo_pago`, `usuario_id`, `proveedor_id`) VALUES
(1, 'FAC-000001', '2025-11-26 06:00:00.000000', 2000.00, 'Efectivo', 2, 1),
(2, 'FAC-000002', '2025-11-27 06:00:00.000000', 3000.00, 'Efectivo', 2, 3),
(3, 'FAC-000003', '2025-11-27 06:00:00.000000', 3500.00, 'Efectivo', 2, 1);

CREATE TABLE `detalle_compras` (
  `id` int NOT NULL,
  `cantidad` int NOT NULL,
  `costo_unitario` decimal(10,2) NOT NULL,
  `subtotal` decimal(10,2) NOT NULL,
  `compra_id` int NOT NULL,
  `libro_id` bigint NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `detalle_compras` (`id`, `cantidad`, `costo_unitario`, `subtotal`, `compra_id`, `libro_id`) VALUES
(1, 10, 200.00, 2000.00, 1, 3),
(2, 10, 100.00, 1000.00, 2, 1),
(3, 10, 200.00, 2000.00, 2, 3),
(4, 5, 500.00, 2500.00, 3, 7),
(5, 5, 200.00, 1000.00, 3, 5);

CREATE TABLE `detalle_ventas` (
  `id` bigint NOT NULL,
  `cantidad` int NOT NULL,
  `precio_unitario` decimal(10,2) NOT NULL,
  `impuesto_unitario` decimal(10,2) NOT NULL,
  `total_linea` decimal(10,2) NOT NULL,
  `libro_id` bigint NOT NULL,
  `venta_id` bigint NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `detalle_ventas` (`id`, `cantidad`, `precio_unitario`, `impuesto_unitario`, `total_linea`, `libro_id`, `venta_id`) VALUES
(1, 1, 0.00, 0.00, 0.00, 3, 1),
(2, 1, 0.00, 0.00, 0.00, 2, 2),
(3, 1, 0.00, 15.00, 0.00, 3, 3),
(4, 1, 0.00, 15.00, 0.00, 1, 4),
(5, 1, 0.00, 15.00, 0.00, 3, 5),
(6, 1, 540.00, 15.00, 621.00, 5, 6),
(7, 1, 300.00, 0.00, 300.00, 1, 7),
(8, 1, 300.00, 15.00, 345.00, 1, 8),
(9, 1, 230.00, 15.00, 264.50, 3, 9),
(10, 1, 540.00, 15.00, 621.00, 5, 10),
(11, 1, 400.00, 15.00, 460.00, 6, 11),
(12, 1, 540.00, 15.00, 621.00, 5, 12),
(13, 1, 500.00, 15.00, 575.00, 8, 13);

CREATE TABLE `django_admin_log` (
  `id` int NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint UNSIGNED NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL
) ;

CREATE TABLE `django_content_type` (
  `id` int NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'auth', 'user'),
(18, 'biblio', 'bitacora'),
(7, 'biblio', 'catalogopublico'),
(8, 'biblio', 'clientes'),
(23, 'biblio', 'compras'),
(24, 'biblio', 'detallecompras'),
(21, 'biblio', 'detalleventa'),
(13, 'biblio', 'ejemplares'),
(9, 'biblio', 'libros'),
(10, 'biblio', 'permisos'),
(14, 'biblio', 'prestamos'),
(22, 'biblio', 'proveedores'),
(11, 'biblio', 'reglasprestamo'),
(15, 'biblio', 'reservas'),
(12, 'biblio', 'roles'),
(16, 'biblio', 'rolpermiso'),
(19, 'biblio', 'solicitudventa'),
(17, 'biblio', 'usuarios'),
(20, 'biblio', 'ventas'),
(5, 'contenttypes', 'contenttype'),
(6, 'sessions', 'session');

CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2025-11-25 18:46:53.998804'),
(2, 'auth', '0001_initial', '2025-11-25 18:46:55.156496'),
(3, 'admin', '0001_initial', '2025-11-25 18:46:55.432114'),
(4, 'admin', '0002_logentry_remove_auto_add', '2025-11-25 18:46:55.442146'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2025-11-25 18:46:55.451721'),
(6, 'contenttypes', '0002_remove_content_type_name', '2025-11-25 18:46:55.622763'),
(7, 'auth', '0002_alter_permission_name_max_length', '2025-11-25 18:46:55.719971'),
(8, 'auth', '0003_alter_user_email_max_length', '2025-11-25 18:46:55.750247'),
(9, 'auth', '0004_alter_user_username_opts', '2025-11-25 18:46:55.761519'),
(10, 'auth', '0005_alter_user_last_login_null', '2025-11-25 18:46:55.843155'),
(11, 'auth', '0006_require_contenttypes_0002', '2025-11-25 18:46:55.850113'),
(12, 'auth', '0007_alter_validators_add_error_messages', '2025-11-25 18:46:55.865115'),
(13, 'auth', '0008_alter_user_username_max_length', '2025-11-25 18:46:55.983996'),
(14, 'auth', '0009_alter_user_last_name_max_length', '2025-11-25 18:46:56.086589'),
(15, 'auth', '0010_alter_group_name_max_length', '2025-11-25 18:46:56.111567'),
(16, 'auth', '0011_update_proxy_permissions', '2025-11-25 18:46:56.124587'),
(17, 'auth', '0012_alter_user_first_name_max_length', '2025-11-25 18:46:56.289874'),
(18, 'biblio', '0001_initial', '2025-11-25 18:46:57.787091'),
(19, 'sessions', '0001_initial', '2025-11-25 18:46:57.849472'),
(20, 'biblio', '0002_solicitudventa_ventas_detalleventa', '2025-11-26 14:47:17.242032'),
(21, 'biblio', '0003_libros_impuesto_porcentaje_libros_precio_venta', '2025-11-26 15:25:36.794267'),
(22, 'biblio', '0004_proveedores_clientes_telefono_usuarios_foto_perfil_and_more', '2025-11-26 19:24:47.551030');

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('3j9h9caxid41jfrpwzf9kxco815xrt8t', '.eJxdjcEKAjEMRP8l50XUY0978D9Ku40SSBtNuqDI_rtRlILHmfeYeQKVuNqalATCcYJFVFFGBalUanOmzCQN-26RChOo8L9D1jUVUafR0Mz1iPcr6QPC3oeZsHWMVCAcRmxSs6JvnFIjZBgEayJ2UD5gvrzj9_2nZJbbin4K4ZzYcHsBSWhKdw:1vO0So:mzuqgldRZG8GxIBlFtmt7r-c7M6DO2HY_CA8fh3yTOw', '2025-12-09 21:20:42.955670'),
('fh31kjjsjbtlgc3ddk7d8d48ovuwjt3i', '.eJxNjU0KQjEMBu-SdRHBjXT1blL6EyWSNpq2oIh3t0-f1OV8GTJPoOR67V5JwB4NRFFFmRNcpOISKDBJwbaLksGACv8p32vD-GEDrmKtQ3d4v5I-wO7HXyYsDR0lsIeJRXJQXDPdF5g7Zk-8zct5ha38EwLLraNPo3_yXPH1BtsKSLA:1vOUIX:ldm8sn4ZcBkH3HYiI7V3TBqmI2qfGmKCx7LHnO2ETww', '2025-12-11 05:12:05.564291'),
('kw0jyq0gqgfpsb31yfwtuv1h66lombwe', '.eJxdyj0KgDAMQOG7ZC4ijp28SehPhkDbSNKCIt7dboLre98NnHHYCMoCfnOQRJXkSxBy5bZHjoWlUV-SVHCgUv6GrWvIovOikdnkSOfBeoFfnxftziZ6:1vO3WK:Bf6RwwjF8sbPj1x9u441fADoavHXOBDDTxLLXO6TTcg', '2025-12-10 00:36:32.630337'),
('lfbqweseh5iavz00rq0ehaty4odp0eq6', '.eJxdyj0KgDAMQOG7ZC4ijp28SehPhkDbSNKCIt7dboLre98NnHHYCMoCfnOQRJXkSxBy5bZHjoWlUV-SVHCgUv6GrWvIovOikdnkSOfBeoFfnxftziZ6:1vONTa:jUwPeR-hUsHRK5Aq8rRjn90x8xSe89n51s0EuPeIV30', '2025-12-10 21:55:02.631446'),
('v86vbxnmx9f2f11lg5o9y718sfak78t7', '.eJxdyj0KgDAMQOG7ZC4ijp28SehPhkDbSNKCIt7dboLre98NnHHYCMoCfnOQRJXkSxBy5bZHjoWlUV-SVHCgUv6GrWvIovOikdnkSOfBeoFfnxftziZ6:1vNyjQ:Do6DoZie6AbXKH2jpqbIX_7TjHj7ZedN9cp7m-uDVLg', '2025-12-09 19:29:44.440720');


CREATE TABLE `ejemplares` (
  `id` bigint NOT NULL,
  `codigo_interno` varchar(50) DEFAULT NULL,
  `ubicacion` varchar(100) DEFAULT NULL,
  `estado` varchar(20) DEFAULT NULL,
  `libro_id` bigint NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `ejemplares` (`id`, `codigo_interno`, `ubicacion`, `estado`, `libro_id`) VALUES
(1, 'EJ-1-6407', 'Estante D1 - Sección Infantil', 'nuevo', 1),
(2, 'EJ-1-5767', 'Estante B2 - Sección Ciencia', 'nuevo', 1),
(3, 'EJ-3-1195', 'Depósito General', 'usado', 3),
(4, 'EJ-3-3847', 'Estante D1 - Sección Infantil', 'usado', 3),
(5, 'EJ-5-1853', 'Depósito General', 'usado', 5),
(6, 'EJ-7-4476', 'Estante C3 - Sección Historia', 'nuevo', 7),
(7, 'EJ-7-7646', 'Estante D1 - Sección Infantil', 'nuevo', 7),
(8, 'EJ-2-7662', 'Depósito General', 'usado', 2),
(9, 'EJ-3-3352', 'Depósito General', 'usado', 3);

CREATE TABLE `libros` (
  `id` bigint NOT NULL,
  `isbn` varchar(20) NOT NULL,
  `titulo` varchar(255) NOT NULL,
  `autor` varchar(255) NOT NULL,
  `categoria` varchar(100) DEFAULT NULL,
  `editorial` varchar(150) DEFAULT NULL,
  `anio_publicacion` longtext,
  `stock_total` int DEFAULT NULL,
  `portada` varchar(100) DEFAULT NULL,
  `fecha_registro` datetime(6) DEFAULT NULL,
  `impuesto_porcentaje` decimal(5,2) NOT NULL,
  `precio_venta` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `libros` (`id`, `isbn`, `titulo`, `autor`, `categoria`, `editorial`, `anio_publicacion`, `stock_total`, `portada`, `fecha_registro`, `impuesto_porcentaje`, `precio_venta`) VALUES
(1, '1234567891012', 'La Ileada de Pedro', 'Miguel Angel', 'ficcion', 'SANTANDER', '1999', 15, 'portadas/1229394_w2LH6fW.jpg', '2025-11-25 19:15:51.500441', 15.00, 300.00),
(2, '1111111111111', 'Siddhartha', 'Herman Hesse', 'ciencia', 'Selector SA', '2000', 13, 'portadas/81VfWIKypvL._UF10001000_QL80_.jpg', '2025-11-25 21:10:00.597494', 15.00, 400.00),
(3, '1122334455123', 'DEMIAN', 'HERMAN HESSE', 'ciencia', 'ECHOES', '1985', 18, 'portadas/demian-50.jpg', '2025-11-25 21:11:01.005961', 15.00, 230.00),
(5, '1234567891011', 'El señor de los anillos: La comunidad del anillo', 'J.R.R. Tolkien', 'ficcion', 'booket', '2001', 24, 'portadas/download.jpg', '2025-11-26 17:02:45.305833', 15.00, 540.00),
(6, '3333555533331', 'El Senor Presidente', 'Menganito', 'ficcion', 'Bolivar', '2000', 4, 'portadas/image.jpg', '2025-11-27 02:48:54.449117', 15.00, 400.00),
(7, '1234567890876', 'IT', 'Stephen King', 'ficcion', 'booket', '1980', 8, 'portadas/images.jpg', '2025-11-27 03:08:55.503266', 15.00, 600.00),
(8, '1234567890999', 'La sombra del Viento', 'Carlos Ruiz Safon', 'ficcion', 'booket', '2001', 9, 'portadas/8249_1_portada___201609051317_1_i63NTWn.jpg', '2025-11-27 05:01:49.054436', 15.00, 500.00);

CREATE TABLE `permisos` (
  `id` bigint NOT NULL,
  `modulo` varchar(100) NOT NULL,
  `accion` varchar(100) NOT NULL,
  `descripcion` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `prestamos` (
  `id` bigint NOT NULL,
  `fecha_inicio` date NOT NULL,
  `fecha_fin` date NOT NULL,
  `fecha_devolucion` date DEFAULT NULL,
  `estado` varchar(20) DEFAULT NULL,
  `cliente_id` bigint NOT NULL,
  `ejemplar_id` bigint NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `prestamos` (`id`, `fecha_inicio`, `fecha_fin`, `fecha_devolucion`, `estado`, `cliente_id`, `ejemplar_id`) VALUES
(1, '2025-11-25', '2025-12-05', '2025-11-25', 'devuelto', 1, 1),
(2, '2025-11-25', '2025-12-31', '2025-11-25', 'devuelto', 1, 2),
(3, '2025-11-26', '2025-12-06', '2025-11-26', 'devuelto', 1, 3),
(4, '2025-11-26', '2025-12-06', '2025-11-26', 'devuelto', 1, 4),
(5, '2025-11-26', '2025-11-27', NULL, 'activo', 1, 5),
(6, '2025-11-26', '2025-12-25', '2025-11-26', 'devuelto', 2, 6),
(7, '2025-11-26', '2025-12-11', NULL, 'activo', 3, 7),
(8, '2025-11-26', '2025-12-11', '2025-11-26', 'devuelto', 3, 8),
(9, '2025-11-28', '2025-12-20', NULL, 'activo', 3, 9);

CREATE TABLE `proveedores` (
  `id` int NOT NULL,
  `nombre_comercial` varchar(150) NOT NULL,
  `rtn` varchar(50) NOT NULL,
  `direccion` varchar(255) DEFAULT NULL,
  `telefono` varchar(50) DEFAULT NULL,
  `correo_contacto` varchar(150) DEFAULT NULL,
  `suministro` varchar(150) DEFAULT NULL,
  `estado` varchar(20) NOT NULL,
  `fecha_registro` datetime(6) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `proveedores` (`id`, `nombre_comercial`, `rtn`, `direccion`, `telefono`, `correo_contacto`, `suministro`, `estado`, `fecha_registro`) VALUES
(1, 'Distribuidora Librera Centroamericana S.A. de C.V.', '08011999012345', 'Boulevard Suyapa, Plaza Los Próceres, Local 12', '22345678', 'ventas@dlibracentro.com', 'Libros físicos y material bibliográfico', 'activo', NULL),
(2, 'Servicios Editoriales y Académicos del Norte', '08011998006789', 'Col. Moderna, 3 calle, 5 avenida, Edificio El Faro', '25123344', 'contacto@seanorte.hn', 'Revistas impresas y suscripciones', 'activo', NULL),
(3, 'Libros Juan y Maria SA de CV', '12345678901234', 'Torre Agalta, Boulevard Morazan, Local 31', '32115201', 'juanmaria@sumshn.com', 'Libros Estudiantiles', 'activo', NULL),
(4, 'Luz y Esperanza', '12345678909991', 'Col Altos de el Trapiche', '32115201', 'luzyfe@esperanza.hn', 'Portafolios y Divisores de Libros', 'activo', NULL);

CREATE TABLE `reglas_prestamo` (
  `id` bigint NOT NULL,
  `plazo_dias` int NOT NULL,
  `limite_prestamos` int NOT NULL,
  `tarifa_mora_diaria` decimal(10,2) NOT NULL,
  `descripcion` varchar(255) DEFAULT NULL,
  `fecha_actualizacion` datetime(6) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `reglas_prestamo` (`id`, `plazo_dias`, `limite_prestamos`, `tarifa_mora_diaria`, `descripcion`, `fecha_actualizacion`) VALUES
(1, 10, 1, 25.00, 'Reglas generales de préstamo', '2025-11-25 19:19:48.205991'),
(2, 1, 2, 25.00, 'Reglas generales de préstamo', '2025-11-26 17:48:29.325102'),
(3, 1, 2, 30.00, 'Reglas generales de préstamo', '2025-11-27 03:05:04.563300'),
(4, 15, 2, 40.00, 'Reglas generales de préstamo', '2025-11-27 03:05:17.893691'),
(5, 10, 3, 50.00, 'Reglas generales de préstamo', '2025-11-27 04:55:30.705529'),
(6, 15, 2, 60.00, 'Reglas generales de préstamo', '2025-11-27 04:59:53.289059');

CREATE TABLE `reservas` (
  `id` bigint NOT NULL,
  `fecha_reserva` datetime(6) DEFAULT NULL,
  `fecha_vencimiento` datetime(6) DEFAULT NULL,
  `estado` varchar(20) DEFAULT NULL,
  `cliente_id` bigint NOT NULL,
  `libro_id` bigint NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


INSERT INTO `reservas` (`id`, `fecha_reserva`, `fecha_vencimiento`, `estado`, `cliente_id`, `libro_id`) VALUES
(1, '2025-11-25 19:47:07.160261', '2025-11-27 19:47:07.160261', 'facturada', 1, 1),
(2, '2025-11-25 21:14:08.428454', '2025-11-27 21:14:08.428454', 'facturada', 1, 3),
(3, '2025-11-26 14:15:23.661784', '2025-11-28 14:15:23.661784', 'facturada', 1, 2),
(4, '2025-11-26 16:43:19.014684', '2025-11-28 16:43:19.014684', 'cancelada', 1, 2),
(5, '2025-11-26 17:12:04.277468', '2025-11-28 17:12:04.277468', 'facturada', 1, 5),
(6, '2025-11-26 17:17:21.534909', '2025-11-28 17:17:21.534909', 'facturada', 1, 1),
(7, '2025-11-26 17:18:43.240104', '2025-11-28 17:18:43.240104', 'facturada', 1, 1),
(8, '2025-11-26 18:50:19.277921', '2025-11-28 18:50:19.277921', 'activa', 1, 2),
(9, '2025-11-27 02:55:44.690847', '2025-11-29 02:55:44.690847', 'facturada', 2, 6),
(10, '2025-11-27 02:56:10.739287', '2025-11-29 02:56:10.739287', 'facturada', 2, 5),
(11, '2025-11-27 04:05:11.894529', '2025-11-29 04:05:11.894529', 'activa', 2, 7),
(12, '2025-11-27 04:05:15.215732', '2025-11-29 04:05:15.215732', 'activa', 2, 6),
(13, '2025-11-27 04:05:17.733196', '2025-11-29 04:05:17.733196', 'activa', 2, 5),
(14, '2025-11-27 04:16:52.219649', '2025-11-29 04:16:52.219649', 'activa', 3, 7),
(15, '2025-11-27 04:17:05.196872', '2025-11-29 04:17:05.196872', 'activa', 3, 6),
(16, '2025-11-27 05:07:53.594981', '2025-11-29 05:07:53.594981', 'activa', 3, 8);

CREATE TABLE `roles` (
  `id` bigint NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `descripcion` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `roles` (`id`, `nombre`, `descripcion`) VALUES
(1, 'cliente', NULL),
(2, 'administrador', 'Administrador general del sistema'),
(3, 'bibliotecario', 'Usuario bibliotecario del sistema');

CREATE TABLE `rol_permiso` (
  `id` int NOT NULL,
  `permiso_id` bigint NOT NULL,
  `rol_id` bigint NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `solicitudes_venta` (
  `id` bigint NOT NULL,
  `cantidad` int NOT NULL,
  `estado` varchar(20) NOT NULL,
  `origen` varchar(20) NOT NULL,
  `fecha_solicitud` datetime(6) NOT NULL,
  `cliente_id` bigint NOT NULL,
  `libro_id` bigint NOT NULL,
  `reserva_id` bigint DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `solicitudes_venta` (`id`, `cantidad`, `estado`, `origen`, `fecha_solicitud`, `cliente_id`, `libro_id`, `reserva_id`) VALUES
(1, 1, 'atendida', 'reserva', '2025-11-26 15:26:56.449496', 1, 2, 3),
(2, 1, 'atendida', 'reserva', '2025-11-26 15:27:36.888639', 1, 3, 2),
(3, 1, 'atendida', 'reserva', '2025-11-26 15:27:39.143863', 1, 1, 1),
(4, 1, 'atendida', 'detalle', '2025-11-26 15:28:28.457688', 1, 3, NULL),
(5, 1, 'atendida', 'detalle', '2025-11-26 16:43:12.112121', 1, 3, NULL),
(6, 1, 'atendida', 'reserva', '2025-11-26 17:12:06.330753', 1, 5, 5),
(7, 1, 'atendida', 'reserva', '2025-11-26 17:17:24.094590', 1, 1, 6),
(8, 1, 'atendida', 'reserva', '2025-11-26 17:18:44.098985', 1, 1, 7),
(9, 1, 'atendida', 'detalle', '2025-11-27 02:56:17.475162', 2, 3, NULL),
(10, 1, 'atendida', 'reserva', '2025-11-27 03:16:02.129623', 2, 5, 10),
(11, 1, 'atendida', 'reserva', '2025-11-27 03:16:07.495743', 2, 6, 9),
(12, 1, 'atendida', 'detalle', '2025-11-27 04:17:12.379175', 3, 5, NULL),
(13, 1, 'atendida', 'detalle', '2025-11-27 05:07:47.546920', 3, 8, NULL);

CREATE TABLE `usuarios` (
  `id` bigint NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `apellido` varchar(100) NOT NULL,
  `email` varchar(150) NOT NULL,
  `clave` varchar(255) NOT NULL,
  `estado` varchar(20) DEFAULT NULL,
  `fecha_creacion` datetime(6) DEFAULT NULL,
  `rol_id` bigint NOT NULL,
  `foto_perfil` varchar(100) DEFAULT NULL,
  `primer_ingreso` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `usuarios` (`id`, `nombre`, `apellido`, `email`, `clave`, `estado`, `fecha_creacion`, `rol_id`, `foto_perfil`, `primer_ingreso`) VALUES
(1, 'Daniel', 'Aguilera', 'daniel@gmail.com', 'pbkdf2_sha256$1000000$QbxkKj3QrgVimuGA0lA4Ee$zRr/Z+TK0idTTKviHdC9xOHxmJ1Op5DzzoDIMlq6EVs=', 'activo', NULL, 1, NULL, 1),
(2, 'Admin', 'Principal', 'admin@biblionet.com', 'pbkdf2_sha256$1000000$NSlIW1wFkMys1vXiF1NZQb$VLRyxAT+ogNUrp3zXpWbNla6uYDe4YlBhOFpZPSiPsw=', 'activo', '2025-11-25 19:08:40.043039', 2, '', 0),
(3, 'Biblio', 'Test', 'biblio@biblionet.com', 'pbkdf2_sha256$1000000$UW8VuvUScGq0VrrCniJaLn$Os1AORwGzIwVrK2Y7nbiBgKqKpvgsMLQt7vOp09Dz/Q=', 'activo', '2025-11-25 19:11:23.976752', 3, '', 0),
(4, 'juana', 'sofia', 'juana@biblionet.com', 'pbkdf2_sha256$1000000$MjHOzOSZdN63RVUms2xMjO$7dAWBZdP3a7oJHoUISYosXq0FoavIrELHLpZlumH3qM=', 'activo', '2025-11-25 19:11:37.472557', 3, NULL, 1),
(5, 'pedro', 'dominguez', 'pedro@gmail.com', 'pbkdf2_sha256$1000000$ZkJJEbABsWmng260a4u0RM$3Ncd0Cj3Q99rsCjKT+8jWqt9t2KpXCUwixo0cmle8Vw=', 'activo', NULL, 1, '', 1),
(6, 'Maria', 'de Arco', 'maria@biblionet.com', 'pbkdf2_sha256$1000000$wKTTv4TXbJG3nOMzo2gABy$SRWH+cDsMizT0s7aWbHkvyZfIEDMUiuWN4vdhrf1m58=', 'activo', '2025-11-27 02:57:58.116978', 3, '', 0),
(7, 'juan', 'mendoza', 'juan@gmail.com', 'pbkdf2_sha256$1000000$193XiXFEJ6k7rOAZUkl11L$Lwq3CB48mlNjxDFem2z1nYmcuUH49zTAr1AW2dm/a+M=', 'activo', NULL, 1, '', 1),
(8, 'Jose', 'iraheta', 'jose@biblionet.com', 'pbkdf2_sha256$1000000$ydgSZ016HHKXQUUYkAfkGs$ATB1mS2jps+DMxoaIP76MHWS7M91ilKefdI2s/ako8M=', 'activo', '2025-11-27 04:18:39.159373', 3, '', 0);

CREATE TABLE `ventas` (
  `id` bigint NOT NULL,
  `fecha_venta` datetime(6) NOT NULL,
  `metodo_pago` varchar(50) NOT NULL,
  `subtotal` decimal(10,2) NOT NULL,
  `impuesto` decimal(10,2) NOT NULL,
  `total` decimal(10,2) NOT NULL,
  `estado` varchar(20) DEFAULT NULL,
  `cliente_id` bigint NOT NULL,
  `vendedor_id` bigint NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `ventas` (`id`, `fecha_venta`, `metodo_pago`, `subtotal`, `impuesto`, `total`, `estado`, `cliente_id`, `vendedor_id`) VALUES
(1, '2025-11-26 15:55:41.638873', 'Efectivo', 0.00, 0.00, 0.00, 'pagada', 1, 3),
(2, '2025-11-26 15:55:54.007602', 'Tarjeta', 0.00, 0.00, 0.00, 'pagada', 1, 3),
(3, '2025-11-26 16:36:35.416718', 'Efectivo', 0.00, 0.00, 0.00, 'pagada', 1, 3),
(4, '2025-11-26 16:38:06.717769', 'Efectivo', 0.00, 0.00, 0.00, 'pagada', 1, 3),
(5, '2025-11-26 16:49:30.793184', 'Efectivo', 0.00, 0.00, 0.00, 'pagada', 1, 3),
(6, '2025-11-26 17:12:18.519318', 'Efectivo', 540.00, 81.00, 621.00, 'pagada', 1, 3),
(7, '2025-11-26 17:17:32.471388', 'Tarjeta', 300.00, 0.00, 300.00, 'pagada', 1, 3),
(8, '2025-11-26 17:18:48.730789', 'Efectivo', 300.00, 45.00, 345.00, 'pagada', 1, 3),
(9, '2025-11-27 03:10:13.006098', 'Efectivo', 230.00, 34.50, 264.50, 'pagada', 2, 6),
(10, '2025-11-27 03:16:39.033869', 'Tarjeta', 540.00, 81.00, 621.00, 'pagada', 2, 6),
(11, '2025-11-27 03:16:42.448718', 'Transferencia', 400.00, 60.00, 460.00, 'pagada', 2, 6),
(12, '2025-11-27 05:03:09.975528', 'Efectivo', 540.00, 81.00, 621.00, 'pagada', 3, 8),
(13, '2025-11-27 05:08:27.555039', 'Efectivo', 500.00, 75.00, 575.00, 'pagada', 3, 8);

ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

ALTER TABLE `auth_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

ALTER TABLE `auth_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  ADD KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`);

ALTER TABLE `auth_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  ADD KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`);

ALTER TABLE `bitacora`
  ADD PRIMARY KEY (`id`),
  ADD KEY `bitacora_usuario_id_e2ff0964_fk_usuarios_id` (`usuario_id`);

ALTER TABLE `clientes`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `dni` (`dni`),
  ADD UNIQUE KEY `usuario_id` (`usuario_id`);

ALTER TABLE `compras`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `numero_factura` (`numero_factura`),
  ADD KEY `compras_usuario_id_b7db04de_fk_usuarios_id` (`usuario_id`),
  ADD KEY `compras_proveedor_id_c6d95402_fk_proveedores_id` (`proveedor_id`);

ALTER TABLE `detalle_compras`
  ADD PRIMARY KEY (`id`),
  ADD KEY `detalle_compras_compra_id_8b19c9c6_fk_compras_id` (`compra_id`),
  ADD KEY `detalle_compras_libro_id_63f8d926_fk_libros_id` (`libro_id`);

ALTER TABLE `detalle_ventas`
  ADD PRIMARY KEY (`id`),
  ADD KEY `detalle_ventas_libro_id_cf593cce_fk_libros_id` (`libro_id`),
  ADD KEY `detalle_ventas_venta_id_a48402cb_fk_ventas_id` (`venta_id`);

ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`);

ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

ALTER TABLE `ejemplares`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `codigo_interno` (`codigo_interno`),
  ADD KEY `ejemplares_libro_id_1acd61ee_fk_libros_id` (`libro_id`);

ALTER TABLE `libros`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `isbn` (`isbn`);

ALTER TABLE `permisos`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `prestamos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `prestamos_cliente_id_324d8020_fk_clientes_id` (`cliente_id`),
  ADD KEY `prestamos_ejemplar_id_d8e2b532_fk_ejemplares_id` (`ejemplar_id`);

ALTER TABLE `proveedores`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `rtn` (`rtn`);

ALTER TABLE `reglas_prestamo`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `reservas`
  ADD PRIMARY KEY (`id`),
  ADD KEY `reservas_cliente_id_ad6386cc_fk_clientes_id` (`cliente_id`),
  ADD KEY `reservas_libro_id_7d0c76cc_fk_libros_id` (`libro_id`);

ALTER TABLE `roles`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `nombre` (`nombre`);

ALTER TABLE `rol_permiso`
  ADD PRIMARY KEY (`id`),
  ADD KEY `rol_permiso_permiso_id_45298b7d_fk_permisos_id` (`permiso_id`),
  ADD KEY `rol_permiso_rol_id_b275ea9d_fk_roles_id` (`rol_id`);

ALTER TABLE `solicitudes_venta`
  ADD PRIMARY KEY (`id`),
  ADD KEY `solicitudes_venta_cliente_id_a7cfd5ce_fk_clientes_id` (`cliente_id`),
  ADD KEY `solicitudes_venta_libro_id_9f6112b9_fk_libros_id` (`libro_id`),
  ADD KEY `solicitudes_venta_reserva_id_b6af9b2a_fk_reservas_id` (`reserva_id`);

ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD KEY `usuarios_rol_id_fa223853_fk_roles_id` (`rol_id`);

ALTER TABLE `ventas`
  ADD PRIMARY KEY (`id`),
  ADD KEY `ventas_cliente_id_30fc3b9d_fk_clientes_id` (`cliente_id`),
  ADD KEY `ventas_vendedor_id_4047adb4_fk_usuarios_id` (`vendedor_id`);

ALTER TABLE `auth_group`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

ALTER TABLE `auth_permission`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=97;

ALTER TABLE `auth_user`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

ALTER TABLE `auth_user_groups`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

ALTER TABLE `auth_user_user_permissions`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

ALTER TABLE `bitacora`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=43;

ALTER TABLE `clientes`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

ALTER TABLE `compras`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

ALTER TABLE `detalle_compras`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

ALTER TABLE `detalle_ventas`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

ALTER TABLE `django_admin_log`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

ALTER TABLE `django_content_type`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

ALTER TABLE `django_migrations`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

ALTER TABLE `ejemplares`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

ALTER TABLE `libros`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

ALTER TABLE `permisos`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

ALTER TABLE `prestamos`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

ALTER TABLE `proveedores`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

ALTER TABLE `reglas_prestamo`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

ALTER TABLE `reservas`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

ALTER TABLE `roles`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

ALTER TABLE `rol_permiso`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

ALTER TABLE `solicitudes_venta`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

ALTER TABLE `usuarios`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

ALTER TABLE `ventas`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

ALTER TABLE `bitacora`
  ADD CONSTRAINT `bitacora_usuario_id_e2ff0964_fk_usuarios_id` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`);

ALTER TABLE `clientes`
  ADD CONSTRAINT `clientes_usuario_id_07f7990e_fk_usuarios_id` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`);

ALTER TABLE `compras`
  ADD CONSTRAINT `compras_proveedor_id_c6d95402_fk_proveedores_id` FOREIGN KEY (`proveedor_id`) REFERENCES `proveedores` (`id`),
  ADD CONSTRAINT `compras_usuario_id_b7db04de_fk_usuarios_id` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`);

ALTER TABLE `detalle_compras`
  ADD CONSTRAINT `detalle_compras_compra_id_8b19c9c6_fk_compras_id` FOREIGN KEY (`compra_id`) REFERENCES `compras` (`id`),
  ADD CONSTRAINT `detalle_compras_libro_id_63f8d926_fk_libros_id` FOREIGN KEY (`libro_id`) REFERENCES `libros` (`id`);

ALTER TABLE `detalle_ventas`
  ADD CONSTRAINT `detalle_ventas_libro_id_cf593cce_fk_libros_id` FOREIGN KEY (`libro_id`) REFERENCES `libros` (`id`),
  ADD CONSTRAINT `detalle_ventas_venta_id_a48402cb_fk_ventas_id` FOREIGN KEY (`venta_id`) REFERENCES `ventas` (`id`);

ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

ALTER TABLE `ejemplares`
  ADD CONSTRAINT `ejemplares_libro_id_1acd61ee_fk_libros_id` FOREIGN KEY (`libro_id`) REFERENCES `libros` (`id`);

ALTER TABLE `prestamos`
  ADD CONSTRAINT `prestamos_cliente_id_324d8020_fk_clientes_id` FOREIGN KEY (`cliente_id`) REFERENCES `clientes` (`id`),
  ADD CONSTRAINT `prestamos_ejemplar_id_d8e2b532_fk_ejemplares_id` FOREIGN KEY (`ejemplar_id`) REFERENCES `ejemplares` (`id`);

ALTER TABLE `reservas`
  ADD CONSTRAINT `reservas_cliente_id_ad6386cc_fk_clientes_id` FOREIGN KEY (`cliente_id`) REFERENCES `clientes` (`id`),
  ADD CONSTRAINT `reservas_libro_id_7d0c76cc_fk_libros_id` FOREIGN KEY (`libro_id`) REFERENCES `libros` (`id`);

ALTER TABLE `rol_permiso`
  ADD CONSTRAINT `rol_permiso_permiso_id_45298b7d_fk_permisos_id` FOREIGN KEY (`permiso_id`) REFERENCES `permisos` (`id`),
  ADD CONSTRAINT `rol_permiso_rol_id_b275ea9d_fk_roles_id` FOREIGN KEY (`rol_id`) REFERENCES `roles` (`id`);

ALTER TABLE `solicitudes_venta`
  ADD CONSTRAINT `solicitudes_venta_cliente_id_a7cfd5ce_fk_clientes_id` FOREIGN KEY (`cliente_id`) REFERENCES `clientes` (`id`),
  ADD CONSTRAINT `solicitudes_venta_libro_id_9f6112b9_fk_libros_id` FOREIGN KEY (`libro_id`) REFERENCES `libros` (`id`),
  ADD CONSTRAINT `solicitudes_venta_reserva_id_b6af9b2a_fk_reservas_id` FOREIGN KEY (`reserva_id`) REFERENCES `reservas` (`id`);

ALTER TABLE `usuarios`
  ADD CONSTRAINT `usuarios_rol_id_fa223853_fk_roles_id` FOREIGN KEY (`rol_id`) REFERENCES `roles` (`id`);

ALTER TABLE `ventas`
  ADD CONSTRAINT `ventas_cliente_id_30fc3b9d_fk_clientes_id` FOREIGN KEY (`cliente_id`) REFERENCES `clientes` (`id`),
  ADD CONSTRAINT `ventas_vendedor_id_4047adb4_fk_usuarios_id` FOREIGN KEY (`vendedor_id`) REFERENCES `usuarios` (`id`);
COMMIT;
