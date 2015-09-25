%global	gem_name	gtksourceview3

Name:		rubygem-%{gem_name}
Version:	2.2.5
Release:	3%{?dist}

Summary:	Ruby binding of gtksourceview-3.x
License:	LGPLv2+

URL:		http://ruby-gnome2.sourceforge.jp/
Source0:	https://rubygems.org/gems/%{gem_name}-%{version}.gem
# https://raw.githubusercontent.com/ruby-gnome2/ruby-gnome2/master/COPYING.LIB
# renamed to avoid namespace collision on sourcedir
Source1:	COPYING.LIB.gtksourceview3

BuildRequires:	ruby-devel
BuildRequires:	rubygems-devel 
BuildRequires:	rubygem-cairo-devel
BuildRequires:	rubygem-glib2-devel
BuildRequires:	rubygem-gtk3-devel
BuildRequires:	pkgconfig(gtksourceview-3.0)
BuildRequires:	rubygem(test-unit)
BuildRequires:	%{_bindir}/xvfb-run

%description
Ruby/GtkSourceView3 is a Ruby binding of gtksourceview-3.x.

%package	doc
Summary:	Documentation for %{name}
Group:	Documentation
Requires:	%{name} = %{version}-%{release}
BuildArch:	noarch

%description	doc
Documentation for %{name}.

%prep
gem unpack %{SOURCE0}
%setup -q -D -T -n  %{gem_name}-%{version}
gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

find . -name \*.rb -print0 | xargs -0 chmod 0644

# Relax ruby-gnome2 internal dependency
sed -i -e 's|= 2\.2\.5|>= 2.2.5|' %{gem_name}.gemspec

sed -i -e 's|test/glib-test-init|glib-test-init|' \
	test/run-test.rb

%build
gem build %{gem_name}.gemspec
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
	%{buildroot}%{gem_dir}/

mkdir -p %{buildroot}%{gem_extdir_mri}
cp -a .%{gem_extdir_mri}/{gem.build_complete,*.so} \
	%{buildroot}%{gem_extdir_mri}/

install -cpm 644 %{SOURCE1} %{buildroot}%{gem_instdir}/COPYING.LIB

pushd %{buildroot}%{gem_instdir}
rm -rf \
	Rakefile \
	extconf.rb \
	ext/ \
	test/ \
	%{nil}

%check
pushd .%{gem_instdir}

rm -rf tmp
mkdir tmp
touch tmp/gtk-test-utils.rb

xvfb-run \
	ruby -Ilib:ext/%{gem_name}:tmp:test ./test/run-test.rb

popd

%files
%dir	%{gem_instdir}
%license	%{gem_instdir}/COPYING.LIB

%{gem_libdir}/
%{gem_extdir_mri}/

%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc	%{gem_docdir}
%doc	%{gem_instdir}/sample/

%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 2.2.5-3
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Apr 29 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.2.5-1
- 2.2.5

* Wed Apr 01 2015 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.2.4-1
- Initial package
