
condlif_poisson = '''
              dV/dt = (El-V + (gfwd+ge)*(Ee-V) + gi*(Ei-V))/tau : volt
              Vt : volt 
              dge /dt = -ge/tau_e : 1
              dgfwd /dt = -gfwd/tau_e : 1
              dgi /dt = -gi/tau_i : 1

              AsumEE : 1
              AsumEI : 1

              ANormTar : 1
              iANormTar : 1
              '''


condlif_memnoise = '''
              dV/dt = (El-V + ge*(Ee-V) + gi*(Ei-V))/tau +  mu/tau + (sigma * xi) / (tau **.5) : volt
              Vt : volt 

              AsumEE : 1
              AsumEI : 1

              sigma: volt (constant)
              mu : volt (constant)

              ANormTar : 1
              iANormTar : 1
              '''

syn_cond_EE_exp = '''
                  dge /dt = -ge/tau_e : 1
                  '''

syn_cond_EI_exp = '''
                  dgi /dt = -gi/tau_i : 1
                  '''

syn_cond_EE_alpha = '''
                    dge /dt = (xge-ge)/tau_e : 1
                    dxge /dt = -xge/tau_e : 1
                    '''

syn_cond_EE_biexp = '''
                    dge/dt = (invpeakEE*xge-ge)/tau_e_rise : 1
                    dxge/dt = -xge/tau_e                   : 1
                    '''

syn_cond_EI_alpha = '''
                    dgi /dt = (xgi-gi)/tau_i : 1
                    dxgi /dt = -xgi/tau_i : 1
                    '''

syn_cond_EI_biexp = '''
                    dgi/dt = (invpeakEI*xgi-gi)/tau_i_rise : 1
                    dxgi/dt = -xgi/tau_i                   : 1
                    '''



# refractory period???

nrnEE_thrshld = 'V > Vt'

nrnEE_reset = 'V = Vr_e'

poisson_mod = 'PInp_a : 1'

# !--- add event-driven for efficiency ---!
# dApre  /dt = -Apre/taupre  : 1 (event-driven)
# dApost /dt = -Apost/taupost : 1 (event-driven)

synEE_static = 'a : 1'
synEE_noise_add   = '''da/dt = syn_active*syn_sigma**0.5*xi : 1
                       syn_sigma : 1/second (shared)'''

synEE_noise_mult  = '''da/dt = syn_active*a*syn_sigma**0.5*xi : 1
                       syn_sigma : 1/second (shared)'''


synEE_mod = '''            
            syn_active : integer

            taupre : second (shared) 
            taupost : second (shared) 

            dApre  /dt = -Apre/taupre  : 1 (event-driven)
            dApost /dt = -Apost/taupost : 1 (event-driven)

            insert_P : 1 (shared) 
            p_inactivate : 1 (shared)
            stdp_active : integer (shared)

            scl_rec_start : second (shared)
            scl_rec_max   : second (shared)

            stdp_rec_start : second (shared)
            stdp_rec_max   : second (shared)

            amax : 1 (shared)
            '''

synEE_scl_mod = 'AsumEE_post = a : 1 (summed)'
synEI_scl_mod = 'AsumEI_post = a : 1 (summed)'


synEE_p_activate = '''
                   r = rand()
                   syn_active = int(r < p_ee)
                   a = syn_active*a
                   '''

synEE_pre_exp   = '''
                  ge_post += syn_active*a
                  Apre = syn_active*Aplus
                  '''

synEE_pre_alpha = '''
                  xge_post += syn_active*a/norm_f_EE
                  Apre = syn_active*Aplus
                  '''

synEE_pre_biexp = '''
                  xge_post += syn_active*a/norm_f_EE
                  Apre = syn_active*Aplus
                  '''


synEI_pre_exp   = '''
                  gi_post += syn_active*a
                  Apre = syn_active*Aplus
                  '''

synEI_pre_alpha = '''
                  xgi_post += syn_active*a/norm_f_EI
                  Apre = syn_active*Aplus
                  '''

synEI_pre_biexp = '''
                  xgi_post += syn_active*a/norm_f_EI
                  Apre = syn_active*Aplus
                  '''


synEI_pre_sym_exp   = '''
                      gi_post += syn_active*a
                      Apre = syn_active*Aplus
                      a = a - stdp_active*LTD_a
                      '''

synEI_pre_sym_alpha = '''
                       xgi_post += syn_active*a/norm_f_EI
                       Apre = syn_active*Aplus
                       a = a - stdp_active*LTD_a
                       '''

synEI_pre_sym_biexp = '''
                       xgi_post += syn_active*a/norm_f_EI
                       Apre = syn_active*Aplus
                       a = a - stdp_active*LTD_a
                       '''


syn_pre_STDP = '''
                 a = syn_active*clip(a+Apost*stdp_active, 0, amax)
                 '''

synEE_pre_rec = '''
                dummy = record_spk(t, i, j, a, Apre, Apost, syn_active, 0, stdp_rec_start, stdp_rec_max)
                '''

synEI_pre_rec = '''
                dummy = record_spk_EI(t, i, j, a, Apre, Apost, syn_active, 0, stdp_rec_start, stdp_rec_max)
                '''


syn_post = '''
           Apost = syn_active*Aminus
           '''

synEI_post_sym = '''
                 Apost = syn_active*Aplus
                 '''


syn_post_STDP = '''
                a = syn_active*clip(a+Apre*stdp_active, 0, amax)
                '''

synEE_post_rec = '''
                 dummy = record_spk(t, i, j, a, Apre, Apost, syn_active, 1, stdp_rec_start, stdp_rec_max)
                 '''

synEI_post_rec = '''
                 dummy = record_spk_EI(t, i, j, a, Apre, Apost, syn_active, 1, stdp_rec_start, stdp_rec_max)
                 '''


synEE_scaling = '''
                a = syn_active*syn_scale(a, ANormTar, AsumEE_post, eta_scaling, t, syn_active, scl_rec_start, scl_rec_max, i, j)
                '''

synEI_scaling = '''
                a = syn_active*syn_EI_scale(a, iANormTar, AsumEI_post, eta_scaling, t, syn_active, scl_rec_start, scl_rec_max, i, j)
                '''


# rand() == uniform(0,1)
#strct_mod = ''

strct_mod_thrs = '''
                 r = rand()
                 should_stay_active = int(a > prn_thrshld)
                 should_become_active = int(r < insert_P)
                 was_active_before = syn_active
                 syn_active = int(syn_active==1) * int(should_stay_active) \
                    + int(syn_active==0) * int(should_become_active)
                 a = a*int(was_active_before==1)*int(syn_active==1) \
                    + a_insert*int(was_active_before==0)*int(syn_active==1)
                 '''

turnover_rec_mod = '''
                   dummy = record_turnover(t, was_active_before, should_become_active, should_stay_active, syn_active, i, j)
                   '''

turnoverEI_rec_mod = '''
                   dummy = record_turnover_EI(t, was_active_before, should_become_active, should_stay_active, syn_active, i, j)
                   '''



strct_mod = '''
            r = rand()
            should_stay_active = int(a > strct_c) + int(a<= strct_c)*int(r>p_inactivate)
            s = rand()
            should_become_active = int(s < insert_P)
            was_active_before = syn_active
            syn_active = int(syn_active==1) * int(should_stay_active) \
                     + int(syn_active==0) * int(should_become_active)
            a = a*int(was_active_before==1)*int(syn_active==1) \
                + a_insert*int(was_active_before==0)*int(syn_active==1)
            '''
