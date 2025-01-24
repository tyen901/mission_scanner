/**
 * Logistics configuration for All in Arma.
 * The configuration is splitted in categories dispatched in the included files.
 */

// Load the logistics config only if the addon is used
if (isClass (configfile >> "CfgPatches" >> "AiA_Core")) then
{
	#include "all_in_arma\air.sqf"
	#include "all_in_arma\landVehicle.sqf"
	#include "all_in_arma\ship.sqf"
	#include "all_in_arma\building.sqf"
	#include "all_in_arma\reammoBox.sqf"
	#include "all_in_arma\others.sqf"
};