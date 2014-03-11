#! /bin/sh

print_help()
{
cat << EOH
Prepares the source tree for configuration

Usage:
  autogen.sh [sydeps [--install]]

Options:

  sysdeps          prints out all dependencies
    --install      install all dependencies ('sudo yum install \$DEPS')

EOH
}

build_depslist()
{
    DEPS_LIST=`grep "^\(Build\)\?Requires:" *.spec.in | grep -v "%{name}" | tr -s " " | tr "," "\n" | cut -f2 -d " " | grep -v "^libreport" | sort -u | tr "\n" " "`
}

case "$1" in
    "--help"|"-h")
            print_help
            exit 0
        ;;
    "sysdeps")
            build_depslist

            if [ "$2" == "--install" ]; then
                set -x verbose
                sudo yum install $DEPS_LIST
                set +x verbose
            else
                echo $DEPS_LIST
            fi
            exit 0
        ;;
    *)
            echo "Running gen-version"
            ./gen-version

            mkdir -p m4
            echo "Creating m4/aclocal.m4 ..."
            test -r m4/aclocal.m4 || touch m4/aclocal.m4

            echo "Running autopoint"
            autopoint --force || exit 1

            echo "Running intltoolize..."
            intltoolize --force --copy --automake || exit 1

            echo "Running aclocal..."
            aclocal || exit 1

            echo "Running libtoolize..."
            libtoolize || exit 1

            echo "Running autoheader..."
            autoheader || return 1

            echo "Running autoconf..."
            autoconf --force || exit 1

            echo "Running automake..."
            automake --add-missing --force --copy || exit 1
        ;;
esac
