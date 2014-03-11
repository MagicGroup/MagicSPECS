/*
   Copyright 2011 Red Hat, Inc.
   All rights reserved.

   Redistribution and use in source and binary forms, with or without
   modification, are permitted provided that the following conditions are met:

    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in
      the documentation and/or other materials provided with the
      distribution.
    * Neither the name of Red Hat, Inc., nor the names of its
      contributors may be used to endorse or promote products derived
      from this software without specific prior written permission.

   THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
   IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
   TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
   PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER
   OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
   EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
   PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
   PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
   LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
   NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
   SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */

/* Walk the list of supplied principal names (or fragments of principal names)
 * and check if the latest kvno on file for that principal has any "strong"
 * keys.  If not, warn in various ways depending on how we were invoked. */

#include <sys/types.h>
#include <getopt.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <kdb.h>

int
main(int argc, char **argv)
{
	char name[256], ename[256], *realm = NULL, *defrealm, *unparsed;
	krb5_context ctx;
	krb5_principal princ;
	krb5_error_code err;
	krb5_db_entry *entry;
	krb5_key_data *kd;
	int problems = 0, c, i, j, verbose = 0, strong, kvno, problems_only = 0;

	while ((c = getopt(argc, argv, "pr:v")) != -1) {
		switch (c) {
		case 'p':
			problems_only++;
			break;
		case 'r':
			realm = optarg;
			break;
		case 'v':
			verbose++;
			break;
		default:
			printf("kdb_check_weak: check if a principal's keys "
			       "are all of types not allowed when\n"
			       "                allow_weak_crypto is not "
			       "set\n");
			printf("%s: [-p | -v [-v [-v]]] [-r REALM] principal [...]\n",
			       strchr(argv[0], '/') ?
			       strrchr(argv[0], '/') + 1 :
			       argv[0]);
			return -1;
			break;
		}
	}

	/* Start up for the default (or specified) realm. */
	ctx = NULL;
	if ((err = krb5_init_context(&ctx)) != 0) {
		fprintf(stderr, "Error initializing Kerberos: %s.\n",
			error_message(err));
		return -1;
	}
	if (realm != NULL) {
		if ((err = krb5_set_default_realm(ctx, realm)) != 0) {
			fprintf(stderr, "Error setting default realm: %s.\n",
				error_message(err));
			return -1;
		}
	}
	defrealm = NULL;
	if ((err = krb5_get_default_realm(ctx, &defrealm)) != 0) {
		fprintf(stderr, "Error getting default realm: %s.\n",
			error_message(err));
		return -1;
	}
	if ((err = krb5_db_open(ctx, NULL, KRB5_KDB_OPEN_RO)) != 0) {
		if (verbose) {
			fprintf(stderr, "Error opening database: %s.\n",
				error_message(err));
		}
		return -1;
	}
	for (i = optind; i < argc; i++) {
		/* Look up the principal. */
		princ = NULL;
		if ((strlen(argv[i]) > 0) &&
		    ((argv[i][strlen(argv[i]) - 1] == '/') ||
		     (argv[i][strlen(argv[i]) - 1] == '@'))) {
			snprintf(name, sizeof(name), "%s%s", argv[i], defrealm);
		} else {
			snprintf(name, sizeof(name), "%s", argv[i]);
		}
		if (krb5_parse_name(ctx, name, &princ) != 0) {
			fprintf(stderr, "Error parsing name \"%s\".\n",
				argv[i]);
			continue;
		}
		entry = NULL;
		if ((err = krb5_db_get_principal(ctx, princ, 0, &entry)) != 0) {
			if (verbose) {
				fprintf(stderr, "Error looking up entry: %s.\n",
					error_message(err));
			}
			continue;
		}
		unparsed = NULL;
		if ((err = krb5_unparse_name(ctx, entry->princ,
					     &unparsed)) != 0) {
			unparsed = name;
		}
		kvno = -1;
		strong = 0;
		for (j = 0; j < entry->n_key_data; j++) {
			kd = &entry->key_data[j];
			/* Reset the count if we find a newer key version. */
			if (kd->key_data_kvno > kvno) {
				kvno = kd->key_data_kvno;
				strong = 0;
			}
			/* Print the types of keys we find if asked to. */
			if (verbose >= 3) {
				krb5_enctype_to_name(kd->key_data_type[0],
						     FALSE,
						     ename, sizeof(ename));
				printf("%s: v%d %s: %s\n",
				       unparsed, kd->key_data_kvno, ename,
				       krb5int_c_weak_enctype(kd->key_data_type[0]) ?
				       "weak" : "strong");
			}
			if (!krb5int_c_weak_enctype(kd->key_data_type[0])) {
				strong++;
			}
		}
		/* We need to have seen some strong keys. */
		if (strong) {
			/* Say we're okay unless we're asked to stay quiet. */
			if (verbose >= 2) {
				printf("%s: OK\n", unparsed);
			}
		} else {
			/* Say we're not okay unless we're asked to stay quiet.
			 * */
			if (verbose) {
				printf("%s: needs to be rekeyed\n", unparsed);
			} else {
				if (problems_only) {
					printf("%s%s", problems ? " " : "",
					       unparsed);
				}
			}
			/* Note that there's a problem entry. */
			problems++;
		}
		krb5_db_free_principal(ctx, entry);
		if (unparsed != name) {
			krb5_free_unparsed_name(ctx, unparsed);
		}
	}

	return problems;
}
