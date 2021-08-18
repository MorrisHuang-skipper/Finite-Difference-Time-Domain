!========================================================
!   Purpose: 1D FDTD simulation in free space with a 
!            Sinusoidal pulse(soft source)
!            with absorbing boundary condition and propagate
!            in a lossy dieletric medium
!
!   Methods: 1D FDTD + absorbing boundary condition
!       
!       Date        Programer       Description of change
!       ====        =========       =====================
!      9/6/20        MorrisH        Original Code
!========================================================
PROGRAM main
    IMPLICIT NONE
    ! number of cells to be used
    INTEGER, PARAMETER :: Ncell = 200
    REAL(8), PARAMETER :: pi = 3.1415927
    REAL(8) :: Ex(Ncell), Hy(Ncell), ca(Ncell), cb(Ncell)
    INTEGER :: k, kc, T, kstart, kfinish
    REAL(8) :: t0, width, pulse, eps, epsz
    REAL(8) :: ddx, dt, freq_in, sigma, eaf
    REAL(8) :: Ex_low_m1 = 0, Ex_high_m1 = 0, &
               Ex_low_m2 = 0, Ex_high_m2 = 0
    ! name of write file
    CHARACTER(len=15) :: str1
    CHARACTER(len=8) :: fmt
    fmt = '(I4.4)'

    ! initialize field
    Ex = 0.0
    Hy = 0.0
    ! center of the problem space
    kc = Ncell / 2
    ! center of the incident pulse
    t0 = 40.0
    ! width of the incident pulse
    width = 12
    ! initialize in free space
    ca = 1.0
    cb = 0.5
    ! epsilon value
    eps = 4
    epsz = 8.85419E-12
    ! start of dielectric medium
    Kstart = 120
    ! end of dielectric medium
    Kfinish = 160
    ! cell size to 1 m
    ddx = 0.01
    ! time step
    dt = ddx / (2 * 3E8)
    ! frequency of input pulse
    freq_in = 700E6
    ! conductivity
    sigma = 0.04

    eaf = dt * sigma / (2 * epsz * eps)

    dielectric: do k = Kstart, Kfinish
        ca(k) = (1.0 - eaf) / (1.0 + eaf)
        cb(k) = 0.5 / (eps * (1.0 + eaf))
    end do dielectric
    
    steploop: do T = 0, 2000

        !!! START FDTD !!!
        ! calculate Ex-field
        Efield: do k = 2, Ncell
            Ex(k) = ca(k) * Ex(k) + cb(k) * (Hy(k-1) - Hy(k))
        end do Efield
        Ex(30) = Ex(30) - 0.5 * sin(2 * pi * freq_in * dt * T)

        ! put gaussian pulse in the center
        pulse = SIN(2 * pi * freq_in * T * dt)
        Ex(30) = Ex(30) + pulse

        ! Absorbing Boundary Condition
        ! Ex(0)_n = Ex(1)_n-2
        Ex(1) = Ex_low_m2
        Ex_low_m2 = Ex_low_m1
        Ex_low_m1 = Ex(2)
        ! Ex(Ncell)_n = Ex(Ncell-1)_n-2
        Ex(Ncell) = Ex_high_m2
        Ex_high_m2 = Ex_high_m1
        Ex_high_m1 = Ex(Ncell-1)

        ! calculate Hy-field
        Hfield: do k = 1, Ncell-1
            Hy(k) = Hy(k) + 0.5 * (Ex(k) - Ex(k+1))
        end do Hfield
        Hy(29) = Hy(29) + 0.5 * sin(2 * pi * freq_in * dt &
                                  * (T - 0.5))
        !!! END FDTD !!!

        ! output Ex and Hy field
        write(str1, fmt) T
        open(1, file='data/Ex_Hy_'//trim(str1)//'.dat', &
             status='unknown')
        output: do k = 1, Ncell
            write(1, *) Ex(k), Hy(k)
        end do output
        close(1)

    end do steploop 
END PROGRAM main
