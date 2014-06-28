open Format;;

(* Minor test from each of the GMP, MPFR modules*)

(* Mpz - integer functions *)

let a = Mpz.init_set_si 2 in
let b = Mpz.init_set_si 3 in
let c = Mpz.init () in
Mpz.add c a b;
Mpz.print std_formatter c;
print_newline ();;

(* Mpq - rational functions *)

let a = Mpq.init () in
let b = Mpq.init () in
let c = Mpq.init () in
let num = Mpz.init () in
Mpq.set_si a 2 3;
Mpq.set_si b 3 4;
Mpq.mul c a b;
Mpq.print std_formatter c; (* We get 1/2 -> appears to "auto-canonicalize"... even internally? *)
print_newline ();
Mpq.get_num num c;
Mpz.print std_formatter num; (* And we get 1 here too... *)
print_newline ();;

(* Mpf - multiprecision floating-point *)

let a = Mpf.init () in
let b = Mpf.init () in
let c = Mpf.init () in
Mpf.set_si a 2;
Mpf.set_si b 3;
Mpf.div c a b;
printf "%.3f" (Mpf.get_d c);
print_newline();;

(* Mpfr - multiprecision floating-point w/rounding *)
(* MPFR library, not GMP library *)

(* Create binary string from floating point number less than 1 *)
(* Use this to test the rounding of Mpfr - the printing function
    they have wasn't working as expected *)
let mpfr_to_bin_str x =
  let (_,one) = Mpfr.init_set_si 1 Mpfr.Near in
  let rec mpfr_to_bin_str_helper x s =
    if Mpfr.cmp_si x 0 = 0 then
      s
    else
      let sp = if Mpfr.cmp_si x 1 >= 0 then
	(let _ = Mpfr.sub x x one Mpfr.Near in "1")
      else
        "0"
      in
      let _ = Mpfr.mul_2si x x 1 Mpfr.Near in
      mpfr_to_bin_str_helper x (s ^ sp) in
  mpfr_to_bin_str_helper x "";;

let a = Mpfr.init() in
let b = Mpfr.init() in
let c = Mpfr.init2 3 in
let _ = Mpfr.set_si a 6875 Mpfr.Near in (* 6875/10000 = 0.1011 in base 2 *)
let _ = Mpfr.set_si b 10000 Mpfr.Near in
let _ = Mpfr.div c a b Mpfr.Near in (* Should round to 0.1100 in precision three *)
print_string (mpfr_to_bin_str c);
print_newline();
let _ = Mpfr.div c a b Mpfr.Down in (* Should round to 0.1010 in precision three *)
print_string (mpfr_to_bin_str c);;
