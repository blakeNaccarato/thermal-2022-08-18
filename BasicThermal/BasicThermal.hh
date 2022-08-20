#ifndef BasicThermal_EXISTS
#define BasicThermal_EXISTS

/**
@attention  Notices

@file  BasicThermal.hh
@brief BasicThermal GUNNS Basic Network declarations.


@details
PURPOSE: (Provides classes for the BasicThermal GUNNS Basic Network.)

REFERENCES:
  ((Item 1)
   (Item 2)
   (Item 3))

ASSUMPTIONS AND LIMITATIONS:
  ((Item 1)
   (Item 2)
   (Item 3))

LIBRARY DEPENDENCY:
  ((BasicThermal.o))

PROGRAMMERS:
  ((Auto-generated by the GunnsDraw netexport script version 19.3.7) (2022-08-19 19:09:43.638839))

@{
*/

#include "software/SimCompatibility/TsSimCompatibility.hh"
#include "core/network/GunnsNetworkBase.hh"
#include "aspects/thermal/GunnsThermalPotential.hh"
#include "core/GunnsBasicConductor.hh"

// Forward-declare the main network class for use in the config data.
class BasicThermal;

////////////////////////////////////////////////////////////////////////////////////////////////////
/// @brief    BasicThermal GUNNS Network Config Data
///
/// @details  Configuration data class for the BasicThermal Network.
////////////////////////////////////////////////////////////////////////////////////////////////////
class BasicThermalConfigData
{
    public:
        // Solver configuration data
        GunnsConfigData netSolver;    /**< (--) trick_chkpnt_io(**) Network solver config data. */ 
        // Spotters configuration data
        // Links configuration data
        GunnsBasicConductorConfigData conductor;    /**< (--) trick_chkpnt_io(**) conductor config data. */
        GunnsThermalPotentialConfigData potential;    /**< (--) trick_chkpnt_io(**) potential config data. */
        /// @brief  Default constructs this network configuration data.
        BasicThermalConfigData(const std::string& name, BasicThermal* network);
        /// @brief  Default destructs this network configuration data.
        virtual ~BasicThermalConfigData();

    private:
        /// @details  Copy constructor unavailable since declared private and not implemented.
        BasicThermalConfigData(const BasicThermalConfigData&);
        /// @details  Assignment operator unavailable since declared private and not implemented.
        BasicThermalConfigData& operator =(const BasicThermalConfigData&);
};

////////////////////////////////////////////////////////////////////////////////////////////////////
/// @brief    BasicThermal GUNNS Network Input Data
///
/// @details  Input data class for the BasicThermal Network.
////////////////////////////////////////////////////////////////////////////////////////////////////
class BasicThermalInputData
{
    public:
        // Spotters input data
        // Links input data
        GunnsBasicConductorInputData conductor;    /**< (--) trick_chkpnt_io(**) conductor input data. */
        GunnsThermalPotentialInputData potential;    /**< (--) trick_chkpnt_io(**) potential input data. */
        /// @brief  Default constructs this network input data.
        BasicThermalInputData(BasicThermal* network);
        /// @brief  Default destructs this network input data.
        virtual ~BasicThermalInputData();

    private:
        /// @details  Copy constructor unavailable since declared private and not implemented.
        BasicThermalInputData(const BasicThermalInputData&);
        /// @details  Assignment operator unavailable since declared private and not implemented.
        BasicThermalInputData& operator =(const BasicThermalInputData&);
};

////////////////////////////////////////////////////////////////////////////////////////////////////
/// @brief    BasicThermal GUNNS Network
///
/// @details  Main class for the BasicThermal Network.
////////////////////////////////////////////////////////////////////////////////////////////////////
class BasicThermal : public GunnsNetworkBase
{
    TS_MAKE_SIM_COMPATIBLE(BasicThermal);
    public:
        /// @brief  Enumeration of the BasicThermal Network nodes.
        enum Nodes
        {
            Node0 = 0,    ///< Node 0
            GROUND = 1,    ///< Ground Node
            N_NODES = 2    ///< Number of nodes including Ground
        };
        // Network declarations
        GunnsBasicNode netNodes[BasicThermal::N_NODES];    /**< (--) Network nodes array. */
        BasicThermalConfigData netConfig;    /**< (--) trick_chkpnt_io(**) Network config data. */
        BasicThermalInputData netInput;    /**< (--) trick_chkpnt_io(**) Network input data. */
        // Data Tables
        // Spotters
        // Links
        GunnsBasicConductor conductor;    /**< (--) conductor instance. */
        GunnsThermalPotential potential;    /**< (--) potential instance. */
        /// @brief  Default constructs this network.
        BasicThermal(const std::string& name = "");
        /// @brief  Default destructs this network.
        virtual ~BasicThermal();
        /// @brief  Network nodes initialization task.
        virtual void initNodes(const std::string& name);
        /// @brief  Network links & spotters initialization task.
        virtual void initNetwork();
        /// @brief  Update network spotters before the solver solution.
        virtual void stepSpottersPre(const double timeStep);
        /// @brief  Update network spotters after the solver solution.
        virtual void stepSpottersPost(const double timeStep);

    private:
        /// @details  Copy constructor unavailable since declared private and not implemented.
        BasicThermal(const BasicThermal&);
        /// @details  Assignment operator unavailable since declared private and not implemented.
        BasicThermal& operator =(const BasicThermal&);
};

/// @}  

#endif
