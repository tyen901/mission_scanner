/* ================================================================================
	GENERAL BRIEFING NOTES
	 - Uses HTML style syntax. All supported tags can be found here - https://community.bistudio.com/wiki/createDiaryRecord
	 - For images use <img image='FILE'></img> (for those familiar with HTML note it is image rather than src).
	 - Note that using the " character inside the briefing block is forbidden use ' instead of ".
*/

/* ================================================================================
	SITUATION
	 - Outline of what is going on, where we are we and what has happened before the mission has started? This needs to contain any relevant background information.
	 - Draw attention to friendly and enemy forces in the area. The commander will make important decisions based off this information.
	 - Outline present weather conditions, players will typically assume that it is daylight with sunny weather.
*/

private _situation = ["diary", ["Situation","
<br/>
<font size='18'>SITUATION</font>
<br/>
15:00:00 Sept 14th 2030, FIA CELL NUT<br/>
<br/>
We are beginning to sabotage AAF military infrastructure along the west coast of altis. We will make a hit and run attack against the town of Negades <marker name='obj2'>Negades. </marker> where AAF forces are storing equipment and vehicles.
<br/><br/>

<font size='18'>ENEMY FORCES</font>
<br/>
The AAF have a mechanized company nearby so you will have to make use of your MAT launchers and escape into the hills before being overwhelmed.
"]];

/* ================================================================================
	MISSION
	 - Describe any objectives that the team is expected to complete.
	 - Summarize(!) the overall task. This MUST be short and clear.
*/

private _mission = ["diary", ["Mission","
<br/>
<font size='18'>MISSION</font>
<br/>
-Destroy 6 ZSU’s within the <marker name='obj1'>marked area.</marker><br/>
-Raid <marker name='obj2'>Negades</marker> and destroy or capture supplies.<br/>
-Retreat north to the mountains.
"]];

/* ================================================================================
	EXECUTION
	 - Provide an outline as to what the commander of the player's command might give.
*/

private _execution = ["diary", ["Execution","
<br/>
<font size='18'>COMMANDER'S INTENT</font>
<br/>
This is a raid and so once your objectives are complete you are free to extract to the north. You may find vehicles to help you in your movement.
<br/><br/>

<font size='18'>MOVEMENT PLAN</font>
<br/>
You start on foot.
<br/>
"]];

/* ================================================================================
	ADMINISTRATION
	 - Outline of logistics: available resources (equipment/vehicles) and ideally a summary of their capabilities.
	 - Outline of how to use any mission specific features/scripts.
	 - Seating capacities of each vehicle available for use.
*/

private _administration = ["diary", ["Administration","
<br/>
You will be able to steal loot off of enemy bodies.
"]];

player createDiaryRecord _administration;
player createDiaryRecord _execution;
player createDiaryRecord _mission;
player createDiaryRecord _situation;