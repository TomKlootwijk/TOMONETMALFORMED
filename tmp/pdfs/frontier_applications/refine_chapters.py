from pathlib import Path
import json
root=Path('C:/TOMONETMALFORMED/output/pdf/frontier_applications_source')
for filename in ('apps_01_06.json','apps_07_12.json','apps_13_18.json'):
    apps=json.loads((root/filename).read_text(encoding='utf-8'))
    for a in apps:
        if a['id']==1:
            a['mechanism']=a['mechanism'].replace('A repair proposal becomes physical history only when the actuator reports actual work; uncertain acknowledgments trigger inspection rather than assumed success.', 'Issued commands enter the record as pending physical events. Acknowledgments and inspection establish what occurred; their absence cannot erase physical effects or justify assuming success.')
        if a['id']==3:
            a['equation']='z_star = argmin_z ||A*z - h_target||^2\nsubject to z_min<=z<=z_max\naccept_support = geometry_ok AND all(f_i<=f_limit_i)\nE_in = integral(sum_i V_i*I_i) dt'
            a['equation_context']='Pin heights z and target heights h are metres; A is a calibrated dimensionless interpolation. After placement, measured forces f in newtons must pass limits for the intended load. Voltage and current determine electrical energy. Feasible geometry alone does not certify stiffness, friction or adhesion.'
        if a['id']==6:
            a['equation_context']='Distances are metres; v_rel bounds relative closing speed throughout latency in seconds. d_stop bounds remaining relative closing distance during stopping, including continued user motion. Tracking error and stopping behavior require measured bounds. This simplified corridor condition needs geometry-specific verification; it cannot alone guarantee collision avoidance.'
        if a['id']==8:
            a['equation']='x_next = argmax_x [IG(x|D)-lambda*Cost(x)]\nsubject to x in ValidCapabilities(state)\ny_next = Measure(Execute(x_next))\nD <- D union {(x_next,y_next)}'
        if a['id']==11:
            a['equation']='M(q)*qddot + C(q,qdot)*qdot + D*qdot\n  + grad_q U(q,latch) = tau + F_ext\nq_target = argmin_q [shape_error + lambda*actuation_cost]\ncommit_latch only if load_path_ok AND measured_lock_ok'
            a['equation_context']='Generalized coordinates q describe joints; U is elastic and gravitational potential for the current latch configuration. M is inertia; C*qdot contains velocity-dependent inertial terms, and D damping. tau and F_ext are actuator and other generalized loads. Travel, stress and stability constrain both targets and transitions.'
        if a['id']==14:
            a['equation']='dW_root/dt = irrigation - uptake - evaporation - drainage\nC_T*dT/dt = Q_light + Q_heat - Q_vent - Q_loss\nP_lamps + P_pumps + P_service <= P_available'
            a['equation_context']='W_root is root-zone water mass, with flows in kilograms per second. Uptake enters plant storage; transpiration is a separate plant loss. C_T is effective thermal capacity and Q terms are watts for a declared boundary. The electrical budget is instantaneous. Crop stress and maintenance require additional models.'
        if a['id']==18:
            a['equation']='b(omega) = S(omega; g,T)*a(omega)\ndg/dt = F(g,u_write,T); y = CoherentReadout(b;reference)\nS^dagger*S <= I  [passive, fixed configuration]'
            a['equation_context']='Here a and b are complex power-normalized amplitudes, g material state and T temperature. This proposed baseline measures phase and amplitude against a calibrated coherent reference. Passivity applies at fixed configuration with appropriate ports. Writing or time modulation requires additional accounting; intensity-only detection does not recover this output.'
            a['source_roles']=a['source_roles'].replace('WANTWOMBAN supplies an optional four-channel transform target, with numerical scaling declared rather than interpreting volume preservation as optical gain.', 'WANTWOMBAN supplies an optional four-channel target with explicit scaling and coherent readout; volume preservation does not imply optical gain.')
            a['demonstrator']=a['demonstrator'].replace('independently measured input and output channels and verified material-state preparation', 'independently measured input/output channels, a stable phase reference, coherent receivers and verified material preparation')
    (root/filename).write_text(json.dumps(apps,indent=2,ensure_ascii=False),encoding='utf-8')
