/* ecc-curves.c  -  Elliptic Curve parameter mangement
 * Copyright (C) 2007, 2008, 2010, 2011 Free Software Foundation, Inc.
 * Copyright (C) 2013 g10 Code GmbH
 *
 * This file is part of Libgcrypt.
 *
 * Libgcrypt is free software; you can redistribute it and/or modify
 * it under the terms of the GNU Lesser General Public License as
 * published by the Free Software Foundation; either version 2.1 of
 * the License, or (at your option) any later version.
 *
 * Libgcrypt is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with this program; if not, see <http://www.gnu.org/licenses/>.
 */

#include <config.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>

#include "g10lib.h"
#include "mpi.h"
#include "cipher.h"
#include "context.h"
#include "ec-context.h"
#include "pubkey-internal.h"
#include "ecc-common.h"


/* This tables defines aliases for curve names.  */
static const struct
{
  const char *name;  /* Our name.  */
  const char *other; /* Other name. */
} curve_aliases[] =
  {
  /*{ "Curve25519", "1.3.6.1.4.1.3029.1.5.1" },*/
    { "Ed25519",    "1.3.6.1.4.1.11591.15.1" },

    { "NIST P-256", "1.2.840.10045.3.1.7" }, /* From NIST SP 800-78-1.  */
    { "NIST P-256", "prime256v1" },
    { "NIST P-256", "secp256r1"  },
    { "NIST P-256", "nistp256"   },          /* rfc5656.  */

    { "NIST P-384", "secp384r1" },
    { "NIST P-384", "1.3.132.0.34" },
    { "NIST P-384", "nistp384"   },          /* rfc5656.  */

    { "NIST P-521", "secp521r1" },
    { "NIST P-521", "1.3.132.0.35" },
    { "NIST P-521", "nistp521"   },          /* rfc5656.  */

    { NULL, NULL}
  };


typedef struct
{
  const char *desc;           /* Description of the curve.  */
  unsigned int nbits;         /* Number of bits.  */
  unsigned int fips:1;        /* True if this is a FIPS140-2 approved curve. */

  /* The model describing this curve.  This is mainly used to select
     the group equation. */
  enum gcry_mpi_ec_models model;

  /* The actual ECC dialect used.  This is used for curve specific
     optimizations and to select encodings etc. */
  enum ecc_dialects dialect;

  const char *p;              /* The prime defining the field.  */
  const char *a, *b;          /* The coefficients.  For Twisted Edwards
                                 Curves b is used for d.  */
  const char *n;              /* The order of the base point.  */
  const char *g_x, *g_y;      /* Base point.  */
} ecc_domain_parms_t;


/* This static table defines all available curves.  */
static const ecc_domain_parms_t domain_parms[] =
  {
    {
      /* (-x^2 + y^2 = 1 + dx^2y^2) */
      "Ed25519", 256, 0,
      MPI_EC_TWISTEDEDWARDS, ECC_DIALECT_ED25519,
      "0x7FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFED",
      "-0x01",
      "-0x2DFC9311D490018C7338BF8688861767FF8FF5B2BEBE27548A14B235ECA6874A",
      "0x1000000000000000000000000000000014DEF9DEA2F79CD65812631A5CF5D3ED",
      "0x216936D3CD6E53FEC0A4E231FDD6DC5C692CC7609525A7B2C9562D608F25D51A",
      "0x6666666666666666666666666666666666666666666666666666666666666658"
    },
    {
      "NIST P-256", 256, 1,
      MPI_EC_WEIERSTRASS, ECC_DIALECT_STANDARD,
      "0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff",
      "0xffffffff00000001000000000000000000000000fffffffffffffffffffffffc",
      "0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b",
      "0xffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc632551",

      "0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296",
      "0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5"
    },
    {
      "NIST P-384", 384, 1,
      MPI_EC_WEIERSTRASS, ECC_DIALECT_STANDARD,
      "0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffe"
      "ffffffff0000000000000000ffffffff",
      "0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffe"
      "ffffffff0000000000000000fffffffc",
      "0xb3312fa7e23ee7e4988e056be3f82d19181d9c6efe8141120314088f5013875a"
      "c656398d8a2ed19d2a85c8edd3ec2aef",
      "0xffffffffffffffffffffffffffffffffffffffffffffffffc7634d81f4372ddf"
      "581a0db248b0a77aecec196accc52973",

      "0xaa87ca22be8b05378eb1c71ef320ad746e1d3b628ba79b9859f741e082542a38"
      "5502f25dbf55296c3a545e3872760ab7",
      "0x3617de4a96262c6f5d9e98bf9292dc29f8f41dbd289a147ce9da3113b5f0b8c0"
      "0a60b1ce1d7e819d7a431d7c90ea0e5f"
    },
    {
      "NIST P-521", 521, 1,
      MPI_EC_WEIERSTRASS, ECC_DIALECT_STANDARD,
      "0x01ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
      "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
      "0x01ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
      "fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffc",
      "0x051953eb9618e1c9a1f929a21a0b68540eea2da725b99b315f3b8b489918ef10"
      "9e156193951ec7e937b1652c0bd3bb1bf073573df883d2c34f1ef451fd46b503f00",
      "0x1fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
      "ffa51868783bf2f966b7fcc0148f709a5d03bb5c9b8899c47aebb6fb71e91386409",

      "0x00c6858e06b70404e9cd9e3ecb662395b4429c648139053fb521f828af606b4d"
      "3dbaa14b5e77efe75928fe1dc127a2ffa8de3348b3c1856a429bf97e7e31c2e5bd66",
      "0x011839296a789a3bc0045c8a5fb42c7d1bd998f54449579b446817afbd17273e"
      "662c97ee72995ef42640c550b9013fad0761353c7086a272c24088be94769fd16650"
    },

    { NULL, 0, 0, 0, 0, NULL, NULL, NULL, NULL }
  };




/* Return a copy of POINT.  */
static gcry_mpi_point_t
point_copy (gcry_mpi_point_t point)
{
  gcry_mpi_point_t newpoint;

  if (point)
    {
      newpoint = mpi_point_new (0);
      point_set (newpoint, point);
    }
  else
    newpoint = NULL;
  return newpoint;
}


/* Helper to scan a hex string. */
static gcry_mpi_t
scanval (const char *string)
{
  gpg_err_code_t rc;
  gcry_mpi_t val;

  rc = _gcry_mpi_scan (&val, GCRYMPI_FMT_HEX, string, 0, NULL);
  if (rc)
    log_fatal ("scanning ECC parameter failed: %s\n", gpg_strerror (rc));
  return val;
}


/* Return the index of the domain_parms table for a curve with NAME.
   Return -1 if not found.  */
static int
find_domain_parms_idx (const char *name)
{
  int idx, aliasno;

  /* First check our native curves.  */
  for (idx = 0; domain_parms[idx].desc; idx++)
    if (!strcmp (name, domain_parms[idx].desc))
      return idx;

  /* If not found consult the alias table.  */
  if (!domain_parms[idx].desc)
    {
      for (aliasno = 0; curve_aliases[aliasno].name; aliasno++)
        if (!strcmp (name, curve_aliases[aliasno].other))
          break;
      if (curve_aliases[aliasno].name)
        {
          for (idx = 0; domain_parms[idx].desc; idx++)
            if (!strcmp (curve_aliases[aliasno].name, domain_parms[idx].desc))
              return idx;
        }
    }

  return -1;
}


/* Generate the crypto system setup.  This function takes the NAME of
   a curve or the desired number of bits and stores at R_CURVE the
   parameters of the named curve or those of a suitable curve.  If
   R_NBITS is not NULL, the chosen number of bits is stored there.
   NULL may be given for R_CURVE, if the value is not required and for
   example only a quick test for availability is desired.  Note that
   the curve fields should be initialized to zero because fields which
   are not NULL are skipped.  */
gpg_err_code_t
_gcry_ecc_fill_in_curve (unsigned int nbits, const char *name,
                         elliptic_curve_t *curve, unsigned int *r_nbits)
{
  int idx;
  const char *resname = NULL; /* Set to a found curve name.  */

  if (name)
    idx = find_domain_parms_idx (name);
  else
    {
      for (idx = 0; domain_parms[idx].desc; idx++)
        if (nbits == domain_parms[idx].nbits
            && domain_parms[idx].model == MPI_EC_WEIERSTRASS)
          break;
      if (!domain_parms[idx].desc)
        idx = -1;
    }
  if (idx < 0)
    return GPG_ERR_UNKNOWN_CURVE;

  resname = domain_parms[idx].desc;

  /* In fips mode we only support NIST curves.  Note that it is
     possible to bypass this check by specifying the curve parameters
     directly.  */
  if (fips_mode () && !domain_parms[idx].fips )
    return GPG_ERR_NOT_SUPPORTED;

  switch (domain_parms[idx].model)
    {
    case MPI_EC_WEIERSTRASS:
    case MPI_EC_TWISTEDEDWARDS:
      break;
    case MPI_EC_MONTGOMERY:
      return GPG_ERR_NOT_SUPPORTED;
    default:
      return GPG_ERR_BUG;
    }


  if (r_nbits)
    *r_nbits = domain_parms[idx].nbits;

  if (curve)
    {
      curve->model = domain_parms[idx].model;
      curve->dialect = domain_parms[idx].dialect;
      if (!curve->p)
        curve->p = scanval (domain_parms[idx].p);
      if (!curve->a)
        curve->a = scanval (domain_parms[idx].a);
      if (!curve->b)
        curve->b = scanval (domain_parms[idx].b);
      if (!curve->n)
        curve->n = scanval (domain_parms[idx].n);
      if (!curve->G.x)
        curve->G.x = scanval (domain_parms[idx].g_x);
      if (!curve->G.y)
        curve->G.y = scanval (domain_parms[idx].g_y);
      if (!curve->G.z)
        curve->G.z = mpi_alloc_set_ui (1);
      if (!curve->name)
        curve->name = resname;
    }

  return 0;
}


/* Give the name of the curve NAME, store the curve parameters into P,
   A, B, G, and N if they point to NULL value.  Note that G is returned
   in standard uncompressed format.  Also update MODEL and DIALECT if
   they are not NULL. */
gpg_err_code_t
_gcry_ecc_update_curve_param (const char *name,
                              enum gcry_mpi_ec_models *model,
                              enum ecc_dialects *dialect,
                              gcry_mpi_t *p, gcry_mpi_t *a, gcry_mpi_t *b,
                              gcry_mpi_t *g, gcry_mpi_t *n)
{
  int idx;

  idx = find_domain_parms_idx (name);
  if (idx < 0)
    return GPG_ERR_UNKNOWN_CURVE;

  if (g)
    {
      char *buf;
      size_t len;

      len = 4;
      len += strlen (domain_parms[idx].g_x+2);
      len += strlen (domain_parms[idx].g_y+2);
      len++;
      buf = xtrymalloc (len);
      if (!buf)
        return gpg_err_code_from_syserror ();
      strcpy (stpcpy (stpcpy (buf, "0x04"), domain_parms[idx].g_x+2),
              domain_parms[idx].g_y+2);
      _gcry_mpi_release (*g);
      *g = scanval (buf);
      xfree (buf);
    }
  if (model)
    *model = domain_parms[idx].model;
  if (dialect)
    *dialect = domain_parms[idx].dialect;
  if (p)
    {
      _gcry_mpi_release (*p);
      *p = scanval (domain_parms[idx].p);
    }
  if (a)
    {
      _gcry_mpi_release (*a);
      *a = scanval (domain_parms[idx].a);
    }
  if (b)
    {
      _gcry_mpi_release (*b);
      *b = scanval (domain_parms[idx].b);
    }
  if (n)
    {
      _gcry_mpi_release (*n);
      *n = scanval (domain_parms[idx].n);
    }
  return 0;
}


/* Return the name matching the parameters in PKEY.  This works only
   with curves described by the Weierstrass equation. */
const char *
_gcry_ecc_get_curve (gcry_sexp_t keyparms, int iterator, unsigned int *r_nbits)
{
  gpg_err_code_t rc;
  const char *result = NULL;
  elliptic_curve_t E;
  gcry_mpi_t mpi_g = NULL;
  gcry_mpi_t tmp = NULL;
  int idx;

  memset (&E, 0, sizeof E);

  if (r_nbits)
    *r_nbits = 0;

  if (!keyparms)
    {
      idx = iterator;
      if (idx >= 0 && idx < DIM (domain_parms))
        {
          result = domain_parms[idx].desc;
          if (r_nbits)
            *r_nbits = domain_parms[idx].nbits;
        }
      return result;
    }


  /*
   * Extract the curve parameters..
   */
  rc = gpg_err_code (sexp_extract_param (keyparms, NULL, "-pabgn",
                                         &E.p, &E.a, &E.b, &mpi_g, &E.n,
                                         NULL));
  if (rc == GPG_ERR_NO_OBJ)
    {
      /* This might be the second use case of checking whether a
         specific curve given by name is supported.  */
      gcry_sexp_t l1;
      char *name;

      l1 = sexp_find_token (keyparms, "curve", 5);
      if (!l1)
        goto leave;  /* No curve name parameter.  */

      name = sexp_nth_string (l1, 1);
      sexp_release (l1);
      if (!name)
        goto leave;  /* Name missing or out of core. */

      idx = find_domain_parms_idx (name);
      xfree (name);
      if (idx >= 0)  /* Curve found.  */
        {
          result = domain_parms[idx].desc;
          if (r_nbits)
            *r_nbits = domain_parms[idx].nbits;
        }
      return result;
    }

  if (rc)
    goto leave;

  if (mpi_g)
    {
      _gcry_mpi_point_init (&E.G);
      if (_gcry_ecc_os2ec (&E.G, mpi_g))
        goto leave;
    }

  for (idx = 0; domain_parms[idx].desc; idx++)
    {
      mpi_free (tmp);
      tmp = scanval (domain_parms[idx].p);
      if (!mpi_cmp (tmp, E.p))
        {
          mpi_free (tmp);
          tmp = scanval (domain_parms[idx].a);
          if (!mpi_cmp (tmp, E.a))
            {
              mpi_free (tmp);
              tmp = scanval (domain_parms[idx].b);
              if (!mpi_cmp (tmp, E.b))
                {
                  mpi_free (tmp);
                  tmp = scanval (domain_parms[idx].n);
                  if (!mpi_cmp (tmp, E.n))
                    {
                      mpi_free (tmp);
                      tmp = scanval (domain_parms[idx].g_x);
                      if (!mpi_cmp (tmp, E.G.x))
                        {
                          mpi_free (tmp);
                          tmp = scanval (domain_parms[idx].g_y);
                          if (!mpi_cmp (tmp, E.G.y))
                            {
                              result = domain_parms[idx].desc;
                              if (r_nbits)
                                *r_nbits = domain_parms[idx].nbits;
                              goto leave;
                            }
                        }
                    }
                }
            }
        }
    }

 leave:
  _gcry_mpi_release (tmp);
  _gcry_mpi_release (E.p);
  _gcry_mpi_release (E.a);
  _gcry_mpi_release (E.b);
  _gcry_mpi_release (mpi_g);
  _gcry_mpi_point_free_parts (&E.G);
  _gcry_mpi_release (E.n);
  return result;
}


/* Helper to extract an MPI from key parameters.  */
static gpg_err_code_t
mpi_from_keyparam (gcry_mpi_t *r_a, gcry_sexp_t keyparam, const char *name)
{
  gcry_err_code_t ec = 0;
  gcry_sexp_t l1;

  l1 = sexp_find_token (keyparam, name, 0);
  if (l1)
    {
      *r_a = sexp_nth_mpi (l1, 1, GCRYMPI_FMT_USG);
      sexp_release (l1);
      if (!*r_a)
        ec = GPG_ERR_INV_OBJ;
    }
  return ec;
}

/* Helper to extract a point from key parameters.  If no parameter
   with NAME is found, the functions tries to find a non-encoded point
   by appending ".x", ".y" and ".z" to NAME.  ".z" is in this case
   optional and defaults to 1.  EC is the context which at this point
   may not be fully initialized. */
static gpg_err_code_t
point_from_keyparam (gcry_mpi_point_t *r_a,
                     gcry_sexp_t keyparam, const char *name, mpi_ec_t ec)
{
  gcry_err_code_t rc;
  gcry_sexp_t l1;
  gcry_mpi_point_t point;

  l1 = sexp_find_token (keyparam, name, 0);
  if (l1)
    {
      gcry_mpi_t a;

      a = sexp_nth_mpi (l1, 1, GCRYMPI_FMT_OPAQUE);
      sexp_release (l1);
      if (!a)
        return GPG_ERR_INV_OBJ;

      point = mpi_point_new (0);
      if (ec && ec->dialect == ECC_DIALECT_ED25519)
        rc = _gcry_ecc_eddsa_decodepoint (a, ec, point, NULL, NULL);
      else
        rc = _gcry_ecc_os2ec (point, a);
      mpi_free (a);
      if (rc)
        {
          mpi_point_release (point);
          return rc;
        }
    }
  else
    {
      char *tmpname;
      gcry_mpi_t x = NULL;
      gcry_mpi_t y = NULL;
      gcry_mpi_t z = NULL;

      tmpname = xtrymalloc (strlen (name) + 2 + 1);
      if (!tmpname)
        return gpg_err_code_from_syserror ();
      strcpy (stpcpy (tmpname, name), ".x");
      rc = mpi_from_keyparam (&x, keyparam, tmpname);
      if (rc)
        {
          xfree (tmpname);
          return rc;
        }
      strcpy (stpcpy (tmpname, name), ".y");
      rc = mpi_from_keyparam (&y, keyparam, tmpname);
      if (rc)
        {
          mpi_free (x);
          xfree (tmpname);
          return rc;
        }
      strcpy (stpcpy (tmpname, name), ".z");
      rc = mpi_from_keyparam (&z, keyparam, tmpname);
      if (rc)
        {
          mpi_free (y);
          mpi_free (x);
          xfree (tmpname);
          return rc;
        }
      if (!z)
        z = mpi_set_ui (NULL, 1);
      if (x && y)
        point = mpi_point_snatch_set (NULL, x, y, z);
      else
        {
          mpi_free (x);
          mpi_free (y);
          mpi_free (z);
          point = NULL;
        }
      xfree (tmpname);
    }

  if (point)
    *r_a = point;
  return 0;
}


/* This function creates a new context for elliptic curve operations.
   Either KEYPARAM or CURVENAME must be given.  If both are given and
   KEYPARAM has no curve parameter, CURVENAME is used to add missing
   parameters.  On success 0 is returned and the new context stored at
   R_CTX.  On error NULL is stored at R_CTX and an error code is
   returned.  The context needs to be released using
   gcry_ctx_release.  */
gpg_err_code_t
_gcry_mpi_ec_new (gcry_ctx_t *r_ctx,
                  gcry_sexp_t keyparam, const char *curvename)
{
  gpg_err_code_t errc;
  gcry_ctx_t ctx = NULL;
  enum gcry_mpi_ec_models model = MPI_EC_WEIERSTRASS;
  enum ecc_dialects dialect = ECC_DIALECT_STANDARD;
  gcry_mpi_t p = NULL;
  gcry_mpi_t a = NULL;
  gcry_mpi_t b = NULL;
  gcry_mpi_point_t G = NULL;
  gcry_mpi_t n = NULL;
  gcry_mpi_point_t Q = NULL;
  gcry_mpi_t d = NULL;
  int flags = 0;
  gcry_sexp_t l1;

  *r_ctx = NULL;

  if (keyparam)
    {
      /* Parse an optional flags list.  */
      l1 = sexp_find_token (keyparam, "flags", 0);
      if (l1)
        {
          errc = _gcry_pk_util_parse_flaglist (l1, &flags, NULL);
          sexp_release (l1);
          l1 = NULL;
          if (errc)
            goto leave;
        }

      /* Check whether a curve name was given.  */
      l1 = sexp_find_token (keyparam, "curve", 5);

      /* If we don't have a curve name or if override parameters have
         explicitly been requested, parse them.  */
      if (!l1 || (flags & PUBKEY_FLAG_PARAM))
        {
          errc = mpi_from_keyparam (&p, keyparam, "p");
          if (errc)
            goto leave;
          errc = mpi_from_keyparam (&a, keyparam, "a");
          if (errc)
            goto leave;
          errc = mpi_from_keyparam (&b, keyparam, "b");
          if (errc)
            goto leave;
          errc = point_from_keyparam (&G, keyparam, "g", NULL);
          if (errc)
            goto leave;
          errc = mpi_from_keyparam (&n, keyparam, "n");
          if (errc)
            goto leave;
        }
    }
  else
    l1 = NULL; /* No curvename.  */

  /* Check whether a curve parameter is available and use that to fill
     in missing values.  If no curve parameter is available try an
     optional provided curvename.  If only the curvename has been
     given use that one. */
  if (l1 || curvename)
    {
      char *name;
      elliptic_curve_t *E;

      if (l1)
        {
          name = sexp_nth_string (l1, 1);
          sexp_release (l1);
          if (!name)
            {
              errc = GPG_ERR_INV_OBJ; /* Name missing or out of core. */
              goto leave;
            }
        }
      else
        name = NULL;

      E = xtrycalloc (1, sizeof *E);
      if (!E)
        {
          errc = gpg_err_code_from_syserror ();
          xfree (name);
          goto leave;
        }

      errc = _gcry_ecc_fill_in_curve (0, name? name : curvename, E, NULL);
      xfree (name);
      if (errc)
        {
          xfree (E);
          goto leave;
        }

      model = E->model;
      dialect = E->dialect;

      if (!p)
        {
          p = E->p;
          E->p = NULL;
        }
      if (!a)
        {
          a = E->a;
          E->a = NULL;
        }
      if (!b)
        {
          b = E->b;
          E->b = NULL;
        }
      if (!G)
        {
          G = mpi_point_snatch_set (NULL, E->G.x, E->G.y, E->G.z);
          E->G.x = NULL;
          E->G.y = NULL;
          E->G.z = NULL;
        }
      if (!n)
        {
          n = E->n;
          E->n = NULL;
        }
      _gcry_ecc_curve_free (E);
      xfree (E);
    }


  errc = _gcry_mpi_ec_p_new (&ctx, model, dialect, flags, p, a, b);
  if (!errc)
    {
      mpi_ec_t ec = _gcry_ctx_get_pointer (ctx, CONTEXT_TYPE_EC);

      if (b)
        {
          mpi_free (ec->b);
          ec->b = b;
          b = NULL;
        }
      if (G)
        {
          ec->G = G;
          G = NULL;
        }
      if (n)
        {
          ec->n = n;
          n = NULL;
        }

      /* Now that we know the curve name we can look for the public key
         Q.  point_from_keyparam needs to know the curve parameters so
         that it is able to use the correct decompression.  Parsing
         the private key D could have been done earlier but it is less
         surprising if we do it here as well.  */
      if (keyparam)
        {
          errc = point_from_keyparam (&Q, keyparam, "q", ec);
          if (errc)
            goto leave;
          errc = mpi_from_keyparam (&d, keyparam, "d");
          if (errc)
            goto leave;
        }

      if (Q)
        {
          ec->Q = Q;
          Q = NULL;
        }
      if (d)
        {
          ec->d = d;
          d = NULL;
        }

      *r_ctx = ctx;
      ctx = NULL;
    }

 leave:
  _gcry_ctx_release (ctx);
  mpi_free (p);
  mpi_free (a);
  mpi_free (b);
  _gcry_mpi_point_release (G);
  mpi_free (n);
  _gcry_mpi_point_release (Q);
  mpi_free (d);
  return errc;
}


/* Return the parameters of the curve NAME as an S-expression.  */
gcry_sexp_t
_gcry_ecc_get_param_sexp (const char *name)
{
  unsigned int nbits;
  elliptic_curve_t E;
  mpi_ec_t ctx;
  gcry_mpi_t g_x, g_y;
  gcry_mpi_t pkey[6];
  gcry_sexp_t result;
  int i;

  memset (&E, 0, sizeof E);
  if (_gcry_ecc_fill_in_curve (0, name, &E, &nbits))
    return NULL;

  g_x = mpi_new (0);
  g_y = mpi_new (0);
  ctx = _gcry_mpi_ec_p_internal_new (MPI_EC_WEIERSTRASS,
                                     ECC_DIALECT_STANDARD,
                                     0,
                                     E.p, E.a, NULL);
  if (_gcry_mpi_ec_get_affine (g_x, g_y, &E.G, ctx))
    log_fatal ("ecc get param: Failed to get affine coordinates\n");
  _gcry_mpi_ec_free (ctx);
  _gcry_mpi_point_free_parts (&E.G);

  pkey[0] = E.p;
  pkey[1] = E.a;
  pkey[2] = E.b;
  pkey[3] = _gcry_ecc_ec2os (g_x, g_y, E.p);
  pkey[4] = E.n;
  pkey[5] = NULL;

  mpi_free (g_x);
  mpi_free (g_y);

  if (sexp_build (&result, NULL,
                  "(public-key(ecc(p%m)(a%m)(b%m)(g%m)(n%m)))",
                  pkey[0], pkey[1], pkey[2], pkey[3], pkey[4]))
    result = NULL;

  for (i=0; pkey[i]; i++)
    _gcry_mpi_release (pkey[i]);

  return result;
}


/* Return an MPI (or opaque MPI) described by NAME and the context EC.
   If COPY is true a copy is returned, if not a const MPI may be
   returned.  In any case mpi_free must be used.  */
gcry_mpi_t
_gcry_ecc_get_mpi (const char *name, mpi_ec_t ec, int copy)
{
  if (!*name)
    return NULL;

  if (!strcmp (name, "p") && ec->p)
    return mpi_is_const (ec->p) && !copy? ec->p : mpi_copy (ec->p);
  if (!strcmp (name, "a") && ec->a)
    return mpi_is_const (ec->a) && !copy? ec->a : mpi_copy (ec->a);
  if (!strcmp (name, "b") && ec->b)
    return mpi_is_const (ec->b) && !copy? ec->b : mpi_copy (ec->b);
  if (!strcmp (name, "n") && ec->n)
    return mpi_is_const (ec->n) && !copy? ec->n : mpi_copy (ec->n);
  if (!strcmp (name, "d") && ec->d)
    return mpi_is_const (ec->d) && !copy? ec->d : mpi_copy (ec->d);

  /* Return a requested point coordinate.  */
  if (!strcmp (name, "g.x") && ec->G && ec->G->x)
    return mpi_is_const (ec->G->x) && !copy? ec->G->x : mpi_copy (ec->G->x);
  if (!strcmp (name, "g.y") && ec->G && ec->G->y)
    return mpi_is_const (ec->G->y) && !copy? ec->G->y : mpi_copy (ec->G->y);
  if (!strcmp (name, "q.x") && ec->Q && ec->Q->x)
    return mpi_is_const (ec->Q->x) && !copy? ec->Q->x : mpi_copy (ec->Q->x);
  if (!strcmp (name, "q.y") && ec->Q && ec->Q->y)
    return mpi_is_const (ec->G->y) && !copy? ec->Q->y : mpi_copy (ec->Q->y);

  /* If the base point has been requested, return it in standard
     encoding.  */
  if (!strcmp (name, "g") && ec->G)
    return _gcry_mpi_ec_ec2os (ec->G, ec);

  /* If the public key has been requested, return it by default in
     standard uncompressed encoding or if requested in other
     encodings.  */
  if (*name == 'q' && (!name[1] || name[1] == '@'))
    {
      /* If only the private key is given, compute the public key.  */
      if (!ec->Q)
        ec->Q = _gcry_ecc_compute_public (NULL, ec, NULL, NULL);

      if (!ec->Q)
        return NULL;

      if (name[1] != '@')
        return _gcry_mpi_ec_ec2os (ec->Q, ec);

      if (!strcmp (name+2, "eddsa") && ec->model == MPI_EC_TWISTEDEDWARDS)
        {
          unsigned char *encpk;
          unsigned int encpklen;

          if (!_gcry_ecc_eddsa_encodepoint (ec->Q, ec, NULL, NULL,
                                            &encpk, &encpklen))
            return mpi_set_opaque (NULL, encpk, encpklen*8);
        }
    }

  return NULL;
}


/* Return a point described by NAME and the context EC.  */
gcry_mpi_point_t
_gcry_ecc_get_point (const char *name, mpi_ec_t ec)
{
  if (!strcmp (name, "g") && ec->G)
    return point_copy (ec->G);
  if (!strcmp (name, "q"))
    {
      /* If only the private key is given, compute the public key.  */
      if (!ec->Q)
        ec->Q = _gcry_ecc_compute_public (NULL, ec, NULL, NULL);

      if (ec->Q)
        return point_copy (ec->Q);
    }

  return NULL;
}


/* Store the MPI NEWVALUE into the context EC under NAME. */
gpg_err_code_t
_gcry_ecc_set_mpi (const char *name, gcry_mpi_t newvalue, mpi_ec_t ec)
{
  gpg_err_code_t rc = 0;

  if (!*name)
    ;
  else if (!strcmp (name, "p"))
    {
      mpi_free (ec->p);
      ec->p = mpi_copy (newvalue);
      _gcry_mpi_ec_get_reset (ec);
    }
  else if (!strcmp (name, "a"))
    {
      mpi_free (ec->a);
      ec->a = mpi_copy (newvalue);
      _gcry_mpi_ec_get_reset (ec);
    }
  else if (!strcmp (name, "b"))
    {
      mpi_free (ec->b);
      ec->b = mpi_copy (newvalue);
    }
  else if (!strcmp (name, "n"))
    {
      mpi_free (ec->n);
      ec->n = mpi_copy (newvalue);
    }
  else if (*name == 'q' && (!name[1] || name[1] == '@'))
    {
      if (newvalue)
        {
          if (!ec->Q)
            ec->Q = mpi_point_new (0);
          if (ec->dialect == ECC_DIALECT_ED25519)
            rc = _gcry_ecc_eddsa_decodepoint (newvalue, ec, ec->Q, NULL, NULL);
          else
            rc = _gcry_ecc_os2ec (ec->Q, newvalue);
        }
      if (rc || !newvalue)
        {
          _gcry_mpi_point_release (ec->Q);
          ec->Q = NULL;
        }
      /* Note: We assume that Q matches d and thus do not reset d.  */
    }
  else if (!strcmp (name, "d"))
    {
      mpi_free (ec->d);
      ec->d = mpi_copy (newvalue);
      if (ec->d)
        {
          /* We need to reset the public key because it may not
             anymore match.  */
          _gcry_mpi_point_release (ec->Q);
          ec->Q = NULL;
        }
    }
  else
   rc = GPG_ERR_UNKNOWN_NAME;

  return rc;
}


/* Store the point NEWVALUE into the context EC under NAME.  */
gpg_err_code_t
_gcry_ecc_set_point (const char *name, gcry_mpi_point_t newvalue, mpi_ec_t ec)
{
  if (!strcmp (name, "g"))
    {
      _gcry_mpi_point_release (ec->G);
      ec->G = point_copy (newvalue);
    }
  else if (!strcmp (name, "q"))
    {
      _gcry_mpi_point_release (ec->Q);
      ec->Q = point_copy (newvalue);
    }
  else
    return GPG_ERR_UNKNOWN_NAME;

  return 0;
}
