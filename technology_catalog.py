"""Curated roadmap of open-source and lower-cost technologies to study."""

from __future__ import annotations

from typing import Any


TECHNOLOGY_ROADMAP: list[dict[str, Any]] = [
    {
        "id": "openmodelica",
        "name": "OpenModelica",
        "category": "Modeling & Simulation",
        "current_stack": "MATLAB/Simulink for physical/system modeling",
        "relationship": "Complement / alternative for Modelica-based system simulation",
        "official_source": "OpenModelica",
        "source_url": "https://openmodelica.org/",
        "overview": (
            "OpenModelica is an open-source Modelica environment for equation-based, "
            "multi-domain system modeling and simulation. It is especially useful for "
            "plant/system models and FMI workflows."
        ),
        "limitations": (
            "It is not a drop-in replacement for the full Simulink, Stateflow, "
            "Embedded Coder, verification, and production-code-generation ecosystem."
        ),
        "learning_goals": ["Modelica", "equation-based modeling", "FMI/FMU", "co-simulation"],
    },
    {
        "id": "scilab-xcos",
        "name": "Scilab + Xcos",
        "category": "Modeling & Simulation",
        "current_stack": "MATLAB + Simulink for numerical work and block-diagram simulation",
        "relationship": "Lower-cost/open-source alternative for selected modeling tasks",
        "official_source": "Scilab",
        "source_url": "https://www.scilab.org/software/xcos",
        "overview": (
            "Scilab provides numerical computing and Xcos provides graphical dynamic "
            "system modeling. It is useful for learning, prototyping, and some control "
            "simulation workflows."
        ),
        "limitations": (
            "Automotive production workflows, qualified code generation, vendor tooling, "
            "and Simulink-compatible libraries are much broader in the MathWorks stack."
        ),
        "learning_goals": ["Xcos blocks", "control simulation", "numerical scripting", "model portability"],
    },
    {
        "id": "python-control",
        "name": "Python Control Systems Library",
        "category": "Controls Engineering",
        "current_stack": "MATLAB Control System Toolbox",
        "relationship": "Open-source alternative for many classical control-analysis tasks",
        "official_source": "python-control",
        "source_url": "https://python-control.readthedocs.io/",
        "overview": (
            "python-control brings transfer functions, state-space models, frequency "
            "response, feedback design, and related control analysis into the Python ecosystem."
        ),
        "limitations": (
            "It does not provide Simulink's graphical production model workflow or the "
            "same integrated automotive code-generation toolchain."
        ),
        "learning_goals": ["state-space", "Bode/Nyquist", "feedback design", "Python scientific stack"],
    },
    {
        "id": "casadi",
        "name": "CasADi",
        "category": "Optimization & MPC",
        "current_stack": "MATLAB optimization and MPC prototyping",
        "relationship": "Complement / alternative for nonlinear optimization and optimal control",
        "official_source": "CasADi",
        "source_url": "https://web.casadi.org/",
        "overview": (
            "CasADi is an open-source framework for algorithmic differentiation and "
            "nonlinear numerical optimization, suited to optimal-control and MPC research."
        ),
        "limitations": (
            "It is a solver-oriented programming framework, not a graphical controls environment "
            "or a complete production ECU development process."
        ),
        "learning_goals": ["optimal control", "nonlinear programming", "automatic differentiation", "MPC"],
    },
    {
        "id": "acados",
        "name": "acados",
        "category": "Optimization & MPC",
        "current_stack": "MATLAB/Simulink MPC prototypes and proprietary optimization solvers",
        "relationship": "Open-source complement for embedded optimal control",
        "official_source": "acados",
        "source_url": "https://docs.acados.org/",
        "overview": (
            "acados is an open-source framework for fast embedded optimal-control and "
            "model-predictive-control algorithms, with interfaces including Python and MATLAB."
        ),
        "limitations": (
            "Integration, safety evidence, scheduling, and target deployment remain engineering "
            "work outside the solver itself."
        ),
        "learning_goals": ["real-time iteration", "MPC", "OCP solvers", "embedded optimization"],
    },
    {
        "id": "fmi-fmu",
        "name": "FMI / FMU",
        "category": "Model Integration",
        "current_stack": "Tool-specific Simulink model exchange and co-simulation",
        "relationship": "Open standard that complements proprietary modeling tools",
        "official_source": "Modelica Association",
        "source_url": "https://fmi-standard.org/",
        "overview": (
            "Functional Mock-up Interface is an open standard for packaging and exchanging "
            "dynamic models as FMUs across simulation tools."
        ),
        "limitations": (
            "FMI standardizes model interfaces and execution packaging; it does not replace "
            "the modeling, calibration, or code-generation tool used to create a model."
        ),
        "learning_goals": ["FMU", "co-simulation", "model exchange", "tool interoperability"],
    },
    {
        "id": "socketcan",
        "name": "SocketCAN + can-utils",
        "category": "Vehicle Networks",
        "current_stack": "CANalyzer/CANoe for CAN monitoring and basic scripting",
        "relationship": "Complement / partial alternative on Linux",
        "official_source": "Linux Kernel",
        "source_url": "https://docs.kernel.org/networking/can.html",
        "overview": (
            "SocketCAN exposes CAN interfaces through the Linux networking stack. Together "
            "with can-utils it enables capture, transmission, logging, replay, and scripting."
        ),
        "limitations": (
            "It does not by itself replace CANoe's full rest-bus simulation, test automation, "
            "diagnostic authoring, database tooling, and vendor integrations."
        ),
        "learning_goals": ["SocketCAN", "candump/cansend", "CAN FD", "Linux networking"],
    },
    {
        "id": "python-can-cantools",
        "name": "python-can + cantools",
        "category": "Vehicle Networks",
        "current_stack": "CANalyzer/CANoe scripting and DBC-based analysis",
        "relationship": "Open-source complement for automated CAN tooling",
        "official_source": "python-can",
        "source_url": "https://python-can.readthedocs.io/",
        "overview": (
            "python-can provides CAN bus access from Python, while cantools adds DBC parsing, "
            "signal encoding/decoding, and related database utilities."
        ),
        "limitations": (
            "Capabilities depend on the CAN interface/backend and require you to assemble "
            "automation, visualization, simulation, and diagnostics as separate components."
        ),
        "learning_goals": ["python-can", "DBC", "cantools", "test automation"],
    },
    {
        "id": "wireshark-automotive",
        "name": "Wireshark for Automotive Ethernet",
        "category": "Vehicle Networks",
        "current_stack": "CANalyzer/CANoe Ethernet and packet inspection",
        "relationship": "Open-source complement for packet-level diagnostics",
        "official_source": "Wireshark",
        "source_url": "https://www.wireshark.org/docs/",
        "overview": (
            "Wireshark is an open-source packet analyzer useful for Automotive Ethernet, "
            "IP, TCP/UDP, SOME/IP-related traffic, DoIP, and general network debugging."
        ),
        "limitations": (
            "Packet analysis is only one part of a complete automotive network simulation "
            "and test environment."
        ),
        "learning_goals": ["pcap", "Ethernet", "TCP/UDP", "DoIP/SOME-IP analysis"],
    },
    {
        "id": "vsomeip",
        "name": "COVESA vsomeip",
        "category": "Service-Oriented Communication",
        "current_stack": "Proprietary SOME/IP middleware and network simulation",
        "relationship": "Open-source SOME/IP implementation for learning and prototyping",
        "official_source": "COVESA",
        "source_url": "https://github.com/COVESA/vsomeip",
        "overview": (
            "vsomeip is an open-source implementation of SOME/IP concepts used to learn "
            "service discovery and service-oriented in-vehicle communication."
        ),
        "limitations": (
            "Production integration still depends on platform requirements, safety/security "
            "constraints, configuration, and OEM/Tier-1 middleware decisions."
        ),
        "learning_goals": ["SOME/IP", "service discovery", "service-oriented architecture", "Ethernet"],
    },
    {
        "id": "covesa-vss",
        "name": "COVESA Vehicle Signal Specification",
        "category": "Vehicle Data",
        "current_stack": "Project-specific signal naming and proprietary vehicle data models",
        "relationship": "Open standard/complement for normalized vehicle data",
        "official_source": "COVESA",
        "source_url": "https://covesa.github.io/vehicle_signal_specification/",
        "overview": (
            "VSS defines a common tree and naming model for vehicle signals, helping decouple "
            "applications and services from proprietary signal naming."
        ),
        "limitations": (
            "VSS is a data model; it does not itself transport signals or replace CAN, SOME/IP, "
            "a VCU application layer, or calibration tooling."
        ),
        "learning_goals": ["vehicle data modeling", "signal namespaces", "SDV APIs", "data abstraction"],
    },
    {
        "id": "iceoryx",
        "name": "Eclipse iceoryx",
        "category": "Middleware",
        "current_stack": "Proprietary ECU/vehicle middleware for high-rate local communication",
        "relationship": "Open-source complement for zero-copy inter-process communication",
        "official_source": "Eclipse iceoryx",
        "source_url": "https://eclipse-iceoryx.github.io/iceoryx/",
        "overview": (
            "iceoryx provides shared-memory, zero-copy IPC for efficient communication "
            "between processes, relevant to high-bandwidth software-defined vehicle platforms."
        ),
        "limitations": (
            "It solves a specific IPC problem and does not replace an entire AUTOSAR, diagnostics, "
            "networking, safety, or application framework."
        ),
        "learning_goals": ["zero-copy IPC", "shared memory", "publish/subscribe", "middleware"],
    },
    {
        "id": "zenoh",
        "name": "Eclipse Zenoh",
        "category": "Middleware",
        "current_stack": "Proprietary distributed data/service middleware",
        "relationship": "Open-source data communication technology to evaluate",
        "official_source": "Eclipse Zenoh",
        "source_url": "https://zenoh.io/",
        "overview": (
            "Zenoh combines pub/sub, query, and storage-oriented data patterns across distributed "
            "systems and is relevant to edge-to-cloud and software-defined vehicle discussions."
        ),
        "limitations": (
            "Suitability for a safety-critical ECU depends on architecture, timing, qualification, "
            "security, and product-specific constraints."
        ),
        "learning_goals": ["pub/sub", "distributed data", "edge/cloud", "QoS"],
    },
    {
        "id": "kuksa",
        "name": "Eclipse KUKSA",
        "category": "Vehicle Data",
        "current_stack": "Proprietary vehicle data brokers and application APIs",
        "relationship": "Open-source complement for SDV vehicle-data access",
        "official_source": "Eclipse KUKSA",
        "source_url": "https://eclipse-kuksa.github.io/kuksa-databroker/",
        "overview": (
            "KUKSA Data Broker exposes vehicle data through standardized interfaces and is "
            "designed around software-defined vehicle data access patterns."
        ),
        "limitations": (
            "It does not replace low-level VCU control loops, CAN drivers, functional-safety "
            "mechanisms, or calibration infrastructure."
        ),
        "learning_goals": ["vehicle data broker", "VSS", "gRPC", "SDV application interfaces"],
    },
    {
        "id": "eclipse-score",
        "name": "Eclipse S-CORE",
        "category": "Automotive Platform",
        "current_stack": "Proprietary automotive platform/middleware components",
        "relationship": "Open-source automotive software foundation to track",
        "official_source": "Eclipse Foundation",
        "source_url": "https://projects.eclipse.org/projects/automotive.score",
        "overview": (
            "Eclipse S-CORE is an automotive open-source initiative aimed at reusable software "
            "building blocks for software-defined vehicle platforms."
        ),
        "limitations": (
            "It is not a single replacement product for MATLAB/Simulink or AUTOSAR, and its "
            "components must be evaluated against project maturity and production requirements."
        ),
        "learning_goals": ["SDV platform", "open-source automotive", "middleware", "platform architecture"],
    },
    {
        "id": "zephyr",
        "name": "Zephyr RTOS",
        "category": "Embedded Runtime",
        "current_stack": "Commercial/proprietary RTOS on embedded controllers",
        "relationship": "Open-source RTOS alternative for appropriate ECU classes",
        "official_source": "Zephyr Project",
        "source_url": "https://docs.zephyrproject.org/",
        "overview": (
            "Zephyr is an open-source real-time operating system with broad MCU support, "
            "networking, drivers, and build tooling."
        ),
        "limitations": (
            "Automotive production use requires hardware support, safety/security strategy, "
            "qualification evidence, and integration appropriate to the ECU."
        ),
        "learning_goals": ["RTOS scheduling", "device tree", "threads", "embedded networking"],
    },
    {
        "id": "threadx",
        "name": "Eclipse ThreadX",
        "category": "Embedded Runtime",
        "current_stack": "Commercial RTOS choices for embedded ECUs",
        "relationship": "Open-source embedded RTOS option to understand",
        "official_source": "Eclipse ThreadX",
        "source_url": "https://eclipse-threadx.github.io/threadx/",
        "overview": (
            "Eclipse ThreadX is an open-source RTOS family for deeply embedded systems and "
            "provides another useful reference point when comparing ECU runtime choices."
        ),
        "limitations": (
            "RTOS selection is only one layer of an automotive ECU and does not replace control "
            "modeling, AUTOSAR services, diagnostics, or safety engineering."
        ),
        "learning_goals": ["RTOS primitives", "determinism", "memory", "embedded middleware"],
    },
    {
        "id": "cyclonedds",
        "name": "Eclipse Cyclone DDS",
        "category": "Middleware",
        "current_stack": "Proprietary publish/subscribe middleware",
        "relationship": "Open-source DDS implementation for distributed systems",
        "official_source": "Eclipse Cyclone DDS",
        "source_url": "https://cyclonedds.io/",
        "overview": (
            "Cyclone DDS implements the OMG DDS publish/subscribe model and is useful for "
            "understanding QoS-driven data distribution in distributed software systems."
        ),
        "limitations": (
            "DDS is not a direct replacement for CAN or every automotive service protocol; "
            "architecture and real-time constraints determine where it fits."
        ),
        "learning_goals": ["DDS", "QoS", "publish/subscribe", "distributed systems"],
    },
    {
        "id": "qemu",
        "name": "QEMU",
        "category": "Virtual ECU & Testing",
        "current_stack": "Hardware-dependent SIL/HIL development and proprietary virtual targets",
        "relationship": "Open-source complement for processor/system virtualization",
        "official_source": "QEMU",
        "source_url": "https://www.qemu.org/docs/master/",
        "overview": (
            "QEMU emulates processors and machine platforms, making it useful for software-first "
            "testing, CI experiments, and some virtual ECU workflows."
        ),
        "limitations": (
            "Timing fidelity, peripheral models, proprietary MCUs, plant models, and HIL I/O may "
            "require commercial tools or custom simulation."
        ),
        "learning_goals": ["emulation", "virtual ECU", "CI testing", "cross compilation"],
    },
    {
        "id": "cmake-gcc-clang",
        "name": "CMake + GCC/Clang",
        "category": "Code-First Embedded Development",
        "current_stack": "Simulink-centric build and generated-code workflow",
        "relationship": "Open-source complement for code-first C/C++ development",
        "official_source": "CMake",
        "source_url": "https://cmake.org/documentation/",
        "overview": (
            "CMake with GCC or Clang represents a common code-first build/toolchain approach "
            "for portable C/C++ software, unit tests, libraries, and CI."
        ),
        "limitations": (
            "A compiler/build system does not replace model-based design, qualified code "
            "generation, requirements traceability, or calibration."
        ),
        "learning_goals": ["CMake", "cross compilation", "GCC/Clang", "static analysis"],
    },
    {
        "id": "pytest-automation",
        "name": "pytest for ECU Test Automation",
        "category": "Testing & CI",
        "current_stack": "Manual/proprietary test scripting around MIL/SIL/HIL tools",
        "relationship": "Open-source complement for automated test orchestration",
        "official_source": "pytest",
        "source_url": "https://docs.pytest.org/",
        "overview": (
            "pytest provides a flexible Python test framework that can orchestrate software tests, "
            "CAN interfaces, diagnostic clients, simulators, and CI pipelines."
        ),
        "limitations": (
            "It is a test framework, not the plant simulator, real-time HIL system, safety case, "
            "or qualified verification tool."
        ),
        "learning_goals": ["fixtures", "parameterization", "CI", "hardware abstraction"],
    },
    {
        "id": "udsoncan-doipclient",
        "name": "udsoncan + doipclient",
        "category": "Diagnostics",
        "current_stack": "CANoe diagnostic tooling and proprietary UDS/DoIP clients",
        "relationship": "Open-source complement for diagnostic automation",
        "official_source": "udsoncan",
        "source_url": "https://udsoncan.readthedocs.io/",
        "overview": (
            "Python diagnostic libraries can script UDS services and DoIP communication for "
            "learning, bench automation, and integration tests."
        ),
        "limitations": (
            "Production diagnostic databases, authoring, conformance testing, security access, "
            "and OEM-specific workflows may require additional commercial tooling."
        ),
        "learning_goals": ["UDS", "DoIP", "diagnostic sessions", "Python automation"],
    },
    {
        "id": "pyxcp",
        "name": "pyXCP",
        "category": "Measurement & Calibration",
        "current_stack": "INCA for XCP measurement and calibration",
        "relationship": "Open-source complement for scripted XCP workflows",
        "official_source": "pyXCP",
        "source_url": "https://pyxcp.readthedocs.io/",
        "overview": (
            "pyXCP is a Python implementation of the ASAM XCP protocol that can support "
            "programmatic measurement/calibration experiments and automation."
        ),
        "limitations": (
            "It does not reproduce INCA's full calibration UI, mature ECU database workflows, "
            "experiment management, vendor integrations, and production support."
        ),
        "learning_goals": ["XCP", "DAQ/STIM concepts", "calibration automation", "ASAM"],
    },
    {
        "id": "asammdf",
        "name": "asammdf",
        "category": "Measurement Data",
        "current_stack": "INCA/MATLAB workflows for MDF measurement-data analysis",
        "relationship": "Open-source complement for MDF processing in Python",
        "official_source": "asammdf",
        "source_url": "https://asammdf.readthedocs.io/",
        "overview": (
            "asammdf reads, writes, converts, filters, and processes ASAM MDF measurement files "
            "inside Python data workflows."
        ),
        "limitations": (
            "It focuses on measurement-file processing and does not replace ECU calibration, "
            "online measurement, or complete experiment management."
        ),
        "learning_goals": ["MDF", "measurement pipelines", "Pandas/Numpy", "data conversion"],
    },
]


def select_next_technology(seen_ids: set[str]) -> dict[str, Any]:
    """Pick the next unseen topic; restart the roadmap after a full cycle."""
    for topic in TECHNOLOGY_ROADMAP:
        if topic["id"] not in seen_ids:
            return topic

    return TECHNOLOGY_ROADMAP[0]
