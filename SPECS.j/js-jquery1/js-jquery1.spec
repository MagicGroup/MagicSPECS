%global commit 9690801db01709bfbff5f977d07fb7cc14472908
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           js-jquery1
Version:        1.11.2
Release:        3%{?dist}
Summary:        JavaScript DOM manipulation, event handling, and AJAX library
BuildArch:      noarch

%global ver_x %(echo %{version} | cut -d. -f1)
%global ver_y %(echo %{version} | cut -d. -f2)
%global ver_z %(echo %{version} | cut -d. -f3)

License:        MIT     
URL:            http://jquery.com/
Source0:        https://github.com/jquery/jquery/archive/%{commit}/%{name}-%{commit}.tar.gz

# disable gzip-js during build
Patch1:         %{name}-disable-gzip-js.patch

BuildRequires:  web-assets-devel
BuildRequires:  nodejs-packaging
BuildRequires:  js-sizzle-static

Provides:       jquery = %{version}-%{release}
Provides:       %{name}-static = %{version}-%{release}

BuildRequires:  nodejs-grunt >= 0.4.4-3
BuildRequires:  npm(shelljs)
BuildRequires:  npm(grunt-cli)
BuildRequires:  npm(grunt-contrib-uglify)
BuildRequires:  npm(load-grunt-tasks)
BuildRequires:  npm(requirejs)

Requires:       web-assets-filesystem

%description
jQuery is a fast, small, and feature-rich JavaScript library. It makes things
like HTML document traversal and manipulation, event handling, animation, and 
Ajax much simpler with an easy-to-use API that works across a multitude of 
browsers. With a combination of versatility and extensibility, jQuery has 
changed the way that millions of people write JavaScript.

%prep
%setup -qn jquery-%{commit}
%patch1 -p1

#remove precompiled stuff
rm -rf dist/* src/sizzle

#put sizzle where jquery expects it
install -Dp %{_jsdir}/sizzle/latest/sizzle.js src/sizzle/dist/sizzle.js


%build
%nodejs_symlink_deps --build
grunt -v 'build:*:*' uglify


# missing dependencies
#%%check
#grunt


%install
%global inslibdir %{buildroot}%{_jsdir}/jquery

mkdir -p %{inslibdir}/%{version}
cp -p dist/* %{inslibdir}/%{version}

mkdir -p %{buildroot}%{_webassetdir}
ln -s ../javascript/jquery %{buildroot}%{_webassetdir}/jquery

ln -s %{version} %{inslibdir}/%{ver_x}
ln -s %{version} %{inslibdir}/%{ver_x}.%{ver_y}


%files
%{_jsdir}/jquery
%{_webassetdir}/jquery
%doc AUTHORS.txt CONTRIBUTING.md MIT-LICENSE.txt README.md


%changelog
* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Mar 05 2015 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.11.2-2
- rebuild with the correct js-sizzle

* Thu Feb 19 2015 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.11.2-1
- new upstream release 1.11.2
  http://blog.jquery.com/2014/12/18/jquery-1-11-2-and-2-1-3-released-safari-fail-safe-edition/

* Tue Oct 21 2014 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.11.1-4
- drop unneccessary symlinks

* Tue Jun 03 2014 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.11.1-3
- follow the github SourceURL guidelines

* Sat May 31 2014 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.11.1-2
- drop sed hack now that grunt is fixed

* Fri May 30 2014 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.11.1-1
- update to 2.1.1
- use system packages for build (with help from Jamie Nguyen)

* Wed Mar 19 2014 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.11.0-0.1
- initial package
