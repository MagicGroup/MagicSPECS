#ifndef OPENCONNECT_OPENSSL
#error Cannot pretend to be compatible if not building with OpenSSL
#endif

#define openconnect_vpninfo_new openconnect_vpninfo_new_with_cbdata
#include "library.c"
#undef openconnect_vpninfo_new

struct openconnect_info *
openconnect_vpninfo_new (char *useragent,
			 openconnect_validate_peer_cert_vfn validate_peer_cert,
			 openconnect_write_new_config_vfn write_new_config,
			 openconnect_process_auth_form_vfn process_auth_form,
			 openconnect_progress_vfn progress);
struct openconnect_info *
openconnect_vpninfo_new (char *useragent,
			 openconnect_validate_peer_cert_vfn validate_peer_cert,
			 openconnect_write_new_config_vfn write_new_config,
			 openconnect_process_auth_form_vfn process_auth_form,
			 openconnect_progress_vfn progress)
{
	return openconnect_vpninfo_new_with_cbdata(useragent,
						   validate_peer_cert,
						   write_new_config,
						   process_auth_form,
						   progress, NULL);
}

void openconnect_init_openssl(void);
void openconnect_init_openssl(void)
{
	openconnect_init_ssl();
}
