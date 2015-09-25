%global	gem_name	webkit-gtk

Name:		rubygem-%{gem_name}
Version:	2.2.5
Release:	3%{?dist}

Summary:	Ruby binding of WebKitGTK+ using GTK3
License:	LGPLv2+
URL: http://ruby-gnome2.sourceforge.jp/
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# https://raw.githubusercontent.com/ruby-gnome2/ruby-gnome2/master/COPYING.LIB
# renamed to avoid namespace collision on sourcedir
Source1:	COPYING.LIB.webkit-gtk

# Require MRI
BuildRequires:	ruby
BuildRequires:	rubygems-devel
BuildRequires:	rubygem-glib2-devel
BuildRequires:	rubygem(gobject-introspection)
BuildRequires:	rubygem(gtk3)
BuildRequires:	rubygem(test-unit)
BuildRequires:	rubygem(test-unit-notify)
BuildRequires:	webkitgtk3
BuildRequires:	%{_bindir}/xvfb-run
Requires:		webkitgtk3

BuildArch:		noarch

%description
Ruby/WebKitGTK is a Ruby binding of WebKitGTK+
using GTK3.

%package	doc
Summary:	Documentation for %{name}
Group:		Documentation
Requires:	%{name} = %{version}-%{release}

%description	doc
Documentation for %{name}.

%prep
gem unpack %{SOURCE0}
%setup -q -D -T -n  %{gem_name}-%{version}

gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

%build
gem build %{gem_name}.gemspec
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
	%{buildroot}%{gem_dir}/

install -cpm 644 %{SOURCE1} %{buildroot}%{gem_instdir}/COPYING.LIB

pushd %{buildroot}%{gem_instdir}
rm -rf \
	Rakefile \
	test/ \
	%{nil}

%check
pushd .%{gem_instdir}
rm -rf tmp
mkdir tmp
pushd tmp
touch gobject-introspection-test-utils.rb
popd

xvfb-run \
	ruby -Ilib:tmp:test ./test/run-test.rb
popd

%files
%dir	%{gem_instdir}
%license	%{gem_instdir}/COPYING.LIB

%{gem_libdir}/
%{gem_spec}

%exclude	%{gem_cache}

%files doc
%doc	%{gem_docdir}/
%doc	%{gem_instdir}/sample/

%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 2.2.5-3
- 为 Magic 3.0 重建

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed May 06 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.2.5-1
- Initial package
