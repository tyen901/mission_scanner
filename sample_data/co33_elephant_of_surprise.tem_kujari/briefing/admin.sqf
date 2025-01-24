
tmf_briefing_admin = "ADMIN BRIEFING<br/><br/>";


/* In this briefing page you should provide the admin with any information that will aid them doing their job.
    - If mission has no automatic ending system. All conditions for the mission ending should be mentioned here so the session host knows what to do.


*/

// Insert custom text
tmf_briefing_admin = tmf_briefing_admin + 
"
- Mission ends when all objectives are complete and the reinforcing OPFOR tanks are destroyed. <br/>
- Players are provided a system to spawn a new TOW Humvee at the initial spawn in the case vehicles are destroyed. <br/>
- Admins may choose to respawn vehicles at their discretion. <br/>
- There is plenty of AA to go around before and at the Dr Jones Airfield encounter; in the case players cannot figure out a solution for rocket Mi-8s is a skill issue. <br/>
";

player createDiaryRecord ["diary", ["Admin", tmf_briefing_admin]];