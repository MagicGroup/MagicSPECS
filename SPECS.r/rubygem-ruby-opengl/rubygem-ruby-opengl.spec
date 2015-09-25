
Summary:	OpenGL Interface for Ruby
%define gem_name ruby-opengl
Name:		rubygem-%{gem_name}
Version:	0.61.0
Release:	4%{?dist}
Group:		Development/Languages
License:	MIT
URL:		http://ruby-opengl.rubyforge.org/
Source0:	https://rubygems.org/gems/%{gem_name}-%{version}.gem

Requires:	ruby(release)
BuildRequires:	ruby(release)
BuildRequires:	rubygems-devel
Requires:	ruby(rubygems)

Requires:	rubygem(opengl)

Provides:	rubygem(%{gem_name}) = %{version}-%{release}
Obsoletes:	ruby-%{gem_name} <= %{version}-%{release}
Provides:	ruby-%{gem_name} = %{version}-%{release}
Provides:	ruby(%{gem_name}) = %{version}-%{release}

# No provides
Obsoletes:	%{name}-doc < 0.60.2

BuildArch:	noarch

%description
ruby-opengl consists of Ruby extension modules that are bindings 
for the OpenGL, GLU, and GLUT libraries. It is intended to be 
a replacement for -- and uses the code from -- Yoshi's ruby-opengl.

%prep
%setup -q -c -T
# Gem repack
TOPDIR=$(pwd)
mkdir tmpunpackdir
pushd tmpunpackdir

gem unpack %{SOURCE0}
cd %{gem_name}-%{version}
gem specification -l --ruby %{SOURCE0} > %{gem_name}.gemspec

gem build %{gem_name}.gemspec
mv %{gem_name}-%{version}.gem $TOPDIR

popd
rm -rf tmpunpackdir

%build
mkdir -p ./%{gem_dir}
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a ./%{gem_dir}/* %{buildroot}%{gem_dir}

# Actually no files
rm -rf %{buildroot}%{gem_docdir}

%files
%exclude	%{gem_cache}
%{gem_spec}

%changelog
* Thu Sep 24 2015 Liu Di <liudidi@gmail.com> - 0.61.0-4
- 为 Magic 3.0 重建

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.61.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.61.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Nov  1 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.61.0-1
- 0.61.0

* Fri Nov  1 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.60.1-14
- Remove files with unclear licenses

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.60.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar  7 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.60.1-12
- F-19: Rebuild for ruby 2.0.0

* Thu Feb  7 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.60.1-11
- Patch for new rake

* Thu Feb  7 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 0.60.1-10
- Don't use STR2CSTR
- Make unneeded deps out of runtime

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.60.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Feb  6 2012 Mamoru Tasaka <mtasaka@fedoraproject.org>  - 0.60.1-7
- F-17: rebuild against f17-ruby

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.60.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.60.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Nov 11 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.60.1-4
- Include ri files

* Sat Jul 25 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.60.1-3
- F-12: Mass rebuild

* Fri Jun 27 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 0.60.1-2
- Initial packaging
